#include "annotate.hpp"

Window::Window(string filename){
    load_image(filename);
    x_sub = image_width/100;
    y_sub = image_height/100;
    //    initialize_points(); 
  }


void Window::load_image(string image_name){
  current_image = imread(image_name); //current image on display   
  current_image_copy = current_image.clone();
  
  image_width = current_image.size().width;
  image_height = current_image.size().height;
  start_x = 0;
  end_x = image_width;
  start_y = 0;
  end_y = image_height;
  zoom_level=0;
}

void Window::zoom_in(){
  int low_x = start_x + x_sub;
  int high_x = end_x - x_sub;
  int low_y = start_y + y_sub;
  int high_y = end_y - y_sub;
  if(low_x < high_x && low_y < high_y){
    start_x = low_x;
    end_x = high_x;
    start_y = low_y;
    end_y = high_y;
    
    zoom_level++;
  }
}

void Window::zoom_out(){
  if(zoom_level>0){
    if(start_x-x_sub < 0){
      start_x = 0;
      end_x += x_sub;
      end_x += x_sub-start_x;
    }
    else if(end_x+x_sub > image_width){
      end_x = image_width;
      start_x -= x_sub;
      start_x -= end_x+x_sub-image_width;
    }
    else{
      start_x -= x_sub;
      end_x += x_sub;
    }
    
    if(start_y-y_sub < 0){
      start_y = 0;
      end_y += y_sub;
      end_y += y_sub-start_y;
    }
    else if(end_y+y_sub > image_height){
      end_y = image_height;
      start_y -= y_sub;
      start_y -= end_y+y_sub-image_height;
    }
    else{
      start_y -= y_sub;
      end_y += y_sub;
    }
    
    zoom_level--; 
    //std::cout<<"zoomout"<<std::endl;
  }  
}

void Window::reset_zoom(){
  start_x = 0;
  end_x = image_width;
  start_y = 0;
  end_y = image_height;
  zoom_level = 0;
}

void Window::update_frame(Point2i p){
  show_points();
  
  //  circle(current_image_copy,p,50,Scalar(0,255,40),6);    
  current_image_copy = current_image_copy(Range(start_y,end_y), Range(start_x,end_x));
  cv::resize(current_image_copy, current_image_copy, current_image.size());
  
  
  
  //shows current coordinate
  show_current_coordinate(p);
    
  imshow("Image",current_image_copy);
  key = waitKey(33);
    
  current_image_copy = current_image.clone();
}

void Window::add_point(Point2i p){
  points.push_back(p);
}

//get pixel (x,y) from window (x,y) of zoomed in screen
cv::Point2i Window::get_coordinate(int x, int y){
  cv::Point2i coordinate(start_x+float(x)*(end_x-start_x)/image_width , start_y+float(y)*(end_y-start_y)/image_height);  
  
  return coordinate;
}

void Window::pan(int del_x, int del_y){
  //decide pan amount based on zoom level
  del_x = del_x*(end_x-start_x)/float(image_width);
  del_y = del_y*(end_y-start_y)/float(image_height);
  
  //pan
  if(del_x!=0){
    
    if(del_x>0){
      //std::cout<<"delx<0"<<std::endl;
      if(start_x-del_x < 0){
	//std::cout<<"delx+startx <0 update"<<std::endl;
	del_x = start_x;
      }
      }
    else{
      if(end_x-del_x > image_width){
	del_x = end_x-image_width;
      }
    }
      
    
    start_x -= del_x;
    end_x -= del_x;
    
    
    //std::cout<<"del_x = "<<del_x<<std::endl;
  }
    
  
  if(del_y!=0){
    
    if(del_y>0){
      if(start_y-del_y < 0){
	  del_y = start_y;
      }
    }
    else{
      if(end_y-del_y > image_height){
	del_y = end_y-image_height;
	}
    }
    
    start_y -= del_y;
    end_y -= del_y;
    
  }
}

void Window::show_points(){
  for(int i=0; i<points.size(); i++){
    //get_coordinate();
    Point2i p = points[i];
    if(p.x>=0 & p.y>=0){
      circle(current_image_copy, points[i],5,color[0],-1);
    }
  }
  
}

void Window::show_current_coordinate(Point2i p){
  rectangle (current_image_copy, Point(0,0),Point(800,150),Scalar(255,255,255),-1);	
  putText(current_image_copy, "( "+to_string(p.x)+", "+to_string(p.y)+" )", cv::Point2i(0,100), FONT_HERSHEY_SIMPLEX,3,Scalar(0,0,0),6);
}

void Window::save_to_file(string filename){        
  ofstream MyFile(filename);

  for(int i=0; i<points.size(); i++){
    Point2f p = points[i];
    string txt_to_write = to_string(p.x) +"\t" + to_string(p.y) +"\n";
    // Write to the file
    MyFile << txt_to_write;
  }

  // Close the file
  MyFile.close();
}                       

void Window::undo(){
  if(points.size()>0){
    points.pop_back();
  }
}
