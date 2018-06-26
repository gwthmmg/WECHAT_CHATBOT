# mg/*int main( int argc, char* argv[] )
{
        std:: ofstream myfile;
      myfile.open ("example.csv");
      myfile << "This is the first cell in the first column.\n";
      myfile << "a,b,c,\n";
      myfile << "c,s,v,\n";
      myfile << "1,2,3.456\n";
      myfile << "semi;colon";
      myfile.close();
      return 0;
}*/
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main( int argc, char* argv[] )
{
    std::ifstream  data("ua.csv");
    std:: ofstream myfile;
    std::string line;
    std::string cell;
    std::string temp;
    FILE * gnuplotPipe = popen ("gnuplot -p", "w");
    fprintf(gnuplotPipe, "%s \n", "set title 'Trajectory\\_ARM'"); 
    while(std::getline(data,line))
    {
        std::stringstream  lineStream(line);
        while(std::getline(lineStream,temp))
        {
        myfile.open("uaa.csv");
        cell+=temp+"\n";
        myfile<<cell<<"\n";
        sleep(1);
        myfile.close();
        fprintf(gnuplotPipe, "%s \n", "plot 'uaa.csv' u 1:2 w lp");       // command 1: plot yvals vs xvals, and Avals vs xvals
        fflush(gnuplotPipe); 
        }
