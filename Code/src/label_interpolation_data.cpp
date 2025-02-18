/*#############################################################################
#  Function to get the (x,y) location of points in image and write them in    #
#  a file as tab separated list of x tab y position. This then can be feed    #
#  into the code that will perform Fourier transform in the data to get the   #
#  frequency information form spatial information. The code will then use     #
#  obtained frequency and amplitude to draw the spatial information that was  #
#  passed.                                                                    #
#                                                                             #
##############################################################################*/

#include "annotate.hpp"


bool record = false; // 
float ix=-1,iy = -1; //variable to keep mouse position.

int x_init = 0;
int y_init = 0;
bool key_press = false;

int del_x = 0;
int del_y = 0;
bool pan = false;

static void onMouse(int event,int x,int y,int,void*)
  {
    
    ix=x;
    iy=y;
    
    if (event == EVENT_LBUTTONDOWN){
      pan = true;
      x_init = x;
      y_init = y;

      if(key_press){
	record = true;
      }
    }
    if(event==EVENT_LBUTTONUP){
      if(pan){
	del_x = x - x_init;
	del_y = y - y_init;
	pan = false;
      }
      
    }
    
  }


int main(int argc, char **argv){
  if(argc==1){
    std::cerr<<"Please use following format and try again"<<std::endl;
    std::cerr<<"./data [target_image_name(png)]"<<std::endl;
    return 1;
  }

  std::cout<<"Press r and left click to record. Press z to undo.  Press ESC to save and exit"<<std::endl;

  std::string image_path = argv[1];
  Window w(image_path);
  std::string output_filename="";
  
  size_t last_slash_pos = image_path.rfind('/');  
  if (last_slash_pos != std::string::npos) {
    // Get the substring before the last '/'
    output_filename = image_path.substr(0, last_slash_pos+1)+"coordinates.txt";
  } else {
    std::cerr << "The character '/' was not found in the string." << std::endl;
  }
    
  namedWindow("Image", cv::WINDOW_NORMAL);
  setMouseCallback("Image",onMouse); //Callback function on mouse click.
    
  while(true){
    
    w.pan(del_x, del_y);
    del_x=0;
    del_y=0;
    cv::Point2i coord = w.get_coordinate(ix, iy);
    if(record){
      w.add_point(coord);
      record=false;
      key_press=false;
    }

    w.update_frame(coord);

        
    if(w.key==171){ //+
      w.zoom_in();
    }

    //zoom out on -
    if(w.key==173){
      w.zoom_out();
    }
    
    //normal view on 0
    if(w.key == 176){
      w.reset_zoom();
    }


    //record
    if(w.key==114){//r
      key_press = true;
      w.point_color = red;
    }

    //undo
    if(w.key==122){//z
      w.undo();
    }
    
    
    
    //std::cout<<"key = "<<w.key<<std::endl;
    if ( w.key == 27) { //waitkey(33) stes to 30 fps because 1000/30 = 33
      std::cout<<"saving "<<output_filename<<std::endl;
      w.save_to_file(output_filename);
      break;
    }
    
  }

  destroyAllWindows();  
  return 0;
}
