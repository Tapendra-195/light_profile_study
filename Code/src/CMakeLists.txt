cmake_minimum_required(VERSION 2.8)
project( data )
find_package(OpenCV 4.0.0 REQUIRED)                                          

add_executable( label_interpolation_data label_interpolation_data.cpp annotate.cpp)
target_link_libraries( label_interpolation_data PRIVATE ${OpenCV_LIBS})

project( augment )
add_executable( augment_data augment.cpp)


