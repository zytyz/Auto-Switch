/*********
  Rui Santos
  Complete project details at http://randomnerdtutorials.com  
*********/

// Load Wi-Fi library
#include <WiFi.h>
#include <Servo.h>

// Replace with your network credentials
const char* ssid     = "ET";
const char* password = "19990512";

// Set web server port number to 80
WiFiServer server(80);
Servo myservo[6];


// Variable to store the HTTP request
String header;

// Auxiliar variables to store the current output state
String output26State = "off";
String output27State = "off";
String output28State = "off";

// Assign output variables to GPIO pins
const int output[6] = {25,26,27,12,13,14};


bool turn(int servoNum,bool state)
{
    if(state == 0)
    {
      myservo[servoNum].write(90);
      delay(1000);
      myservo[servoNum].write(125);
      delay(1000);
      myservo[servoNum].write(90);
      delay(1000);
      Serial.println("turned 1");
      return true;
    }
    else if(state ==1)
    {
      myservo[servoNum].write(90);
      delay(1000);
      myservo[servoNum].write(65);
      delay(1000);
      myservo[servoNum].write(90);
      delay(1000);
      Serial.println("turned 2");
      return true;
    }

    
}


void setup() {
  Serial.begin(115200);
  // Initialize the output variables as outputs
  
  // Set outputs to LOW
  for(int i=0;i<6;++i)
  {
    myservo[i].attach(output[i]);
  }

  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop(){
  WiFiClient client = server.available();   //Gets a client that is connected to the server and has data available for reading
  // Listen for incoming clients

  if (client) {                             // If a new client connects,
    Serial.println("New Client.");          // print a message out in the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected())              // loop while the client's connected
    {  //client.connected(): Connects to a specified IP address and port           
      if (client.available()) // if there's bytes to read from the client,
      {             
        //client.available(): Returns the number of bytes available for reading
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        //Serial.print(c) Serial.print(c) is the same except print() is about ascii code
        header += c;
        if (c == '\n') 
        {                    // if the byte is a newline character
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) 
          {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();
            
            // turns the GPIOs on and off
            if (header.indexOf("GET /26/on") >= 0) 
            {
              Serial.println("GPIO 26 on");
              output26State = "on";
              turn(0,1);

            } 
            else if (header.indexOf("GET /26/off") >= 0) 
            {
              Serial.println("GPIO 26 off");
              output26State = "off";
              turn(1,0);
            } 
            else if (header.indexOf("GET /27/on") >= 0) 
            {
              Serial.println("GPIO 27 on");
              output27State = "on";
              turn(2,0);
            } 
            else if (header.indexOf("GET /27/off") >= 0) 
            {
              Serial.println("GPIO 27 off");
              output27State = "off";
              turn(3,1);
            }
            else if (header.indexOf("GET /28/on") >= 0) 
            {
              Serial.println("GPIO 28 on");
              output28State = "on";
              turn(4,0);
            } 
            else if (header.indexOf("GET /28/off") >= 0) 
            {
              Serial.println("GPIO 28 off");
              output28State = "off";
              turn(5,1);
            }
            
            // Display the HTML web page
            client.println("<!DOCTYPE html><html>");
            client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            client.println("<link rel=\"icon\" href=\"data:,\">");
            // CSS to style the on/off buttons 
            // Feel free to change the background-color and font-size attributes to fit your preferences
            client.println("<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}");
            client.println(".button { background-color: #4CAF50; border: none; color: white; padding: 16px 40px;");
            client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");
            client.println(".button2 {background-color: #555555;}</style></head>");
            
            // Web Page Heading
            client.println("<body><h1>Automatic Switch</h1>");
            
            // Display current state, and ON/OFF buttons for GPIO 26  
            client.println("<p> Switch One " + output26State + "</p>");
            // If the output26State is off, it displays the ON button       
            if (output26State=="off") 
            {
              client.println("<p><a href=\"/26/on\"><button name=\"First_Button\" class=\"button\">ON</button></a></p>");
            }
            else 
            {
              client.println("<p><a href=\"/26/off\"><button name=\"First_Button\" class=\"button button2\">OFF</button></a></p>");
            } 
               
            // Display current state, and ON/OFF buttons for GPIO 27  
            client.println("<p> Switch Two " + output27State + "</p>");
            // If the output27State is off, it displays the ON button       
            if (output27State=="off") 
            {
              client.println("<p><a href=\"/27/on\"><button name=\"Second_Button\" class=\"button\">ON</button></a></p>");
            } 
            else 
            {
              client.println("<p><a href=\"/27/off\"><button name=\"Second_Button\" class=\"button name=\"Second_Button\" button2\">OFF</button></a></p>");
            }
            // Display current state, and ON/OFF buttons for GPIO 27  
            client.println("<p> Switch Three " + output28State + "</p>");
            // If the output28State is off, it displays the ON button       
            if (output28State=="off") 
            {
              client.println("<p><a href=\"/28/on\"><button name=\"Third_Button\" class=\"button\">ON</button></a></p>");
            } 
            else 
            {
              client.println("<p><a href=\"/28/off\"><button name=\"Third_Button\" class=\"button button2\">OFF</button></a></p>");
            }
            client.println("</body></html>");
            
            // The HTTP response ends with another blank line
            client.println();
            // Break out of the while loop
            break;
          } 
          else 
          { // if you got a newline, then clear currentLine
            currentLine = "";
          }
        } 
        else if (c != '\r') 
        {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
      }
    }
    // Clear the header variable
    header = "";
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
