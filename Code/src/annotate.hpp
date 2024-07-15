#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <stdio.h>
#include <opencv2/features2d.hpp>
#include <fstream>
#include <string>

using namespace cv;
using namespace std;

enum colors { red, green, blue, yellow};

class Window{
public:
  int image_width;
  int image_height;
  int start_x;// = 0;
  int end_x;// = imageWidth;
  int start_y;// = 0;
  int end_y;// = imageHeight;
  int x_sub;// = imageWidth/100.;
  int y_sub;// = imageHeight/100.;
  int zoom_level;
  int key;  
  std::vector<Point2i> points;
  Scalar color[4] = {Scalar(0,0,255),Scalar(0,255,0), Scalar(255,0,0), Scalar(0,255,255)};
  int point_color = -1;
  Mat current_image;
  Mat current_image_copy;
    
  Window(string filename);
  void initialize_points();
  void zoom_in();
  void zoom_out();
  void reset_zoom();
  void update_frame(Point2i p);
  void add_point(Point2i p);
  //get pixel (x,y) from window (x,y) of zoomed in screen
  cv::Point2i get_coordinate(int x, int y);
  void pan(int del_x, int del_y);
  void save_to_file(string filename = "coordinates.txt");
  void undo();
private:  
  void load_image(string image_name);
  void show_points();
  void show_current_coordinate(Point2i p);
};

