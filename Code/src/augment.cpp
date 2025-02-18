/*########################################################################
#  Takes a output text file from data program with (u,v) coordinate and  #
#  saves a augmented text file with corresponding x and y appended.      #
########################################################################*/

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
using namespace std;


int main(int argc, char* argv[]) {
  if (argc < 3) {
    std::cerr << "Usage: " << argv[0] << "<filename> <columns>" << std::endl;
    return 1;
  }
  
  std::string file_path = argv[1];
  int cols = std::atoi(argv[2]);

  if (cols <= 0) {
    std::cerr << "Columns must be positive integers." << std::endl;
    return 1;
  }  
  
  std::string output_filename="";
  
  size_t last_dot_pos = file_path.rfind('.');  
  if (last_dot_pos != std::string::npos) {
    // Get the substring before the last '/'
    output_filename = file_path.substr(0, last_dot_pos)+"_augmented.txt";
  } else {
    std::cerr << "The character '.' was not found in the string." << std::endl;
  }
    
  
  string myText;
  ifstream MyReadFile(file_path);
  ofstream MyWriteFile(output_filename);  

  std::cout<<"reading "<<file_path<<std::endl;
  
  int i=0;
  while (getline (MyReadFile, myText)) {
    // Output the text from the file
    string u = myText.substr(0,myText.find('\t')+1);
    string v = myText.substr(myText.find("\t")+1);;

    int x = i%cols;
    int y = i/cols;

    cout<<"(u,v) = "<<"("<<u<<", "<<v<<")"<<endl;
    cout<<"(x,y) = "<<"("<<x<<", "<<y<<")"<<endl;

    MyWriteFile<<u<<"\t"<<v<<"\t"<<x<<"\t"<<y<<std::endl;    

    i++;
  }

  std::cout<<"Saving to "<<output_filename<<std::endl;
  
  MyReadFile.close();
  MyWriteFile.close();
  
  return 0;
}
