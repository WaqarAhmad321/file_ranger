#ifndef FILE_NODE_H
#define FILE_NODE_H

#include<iostream>
#include<vector>
#include<string>
#include<memory>

using std::string;
using std::vector;
using std::shared_ptr;


struct FileNode {
    string name;
    string path;
    bool is_directory;
    size_t size;
    vector<shared_ptr<FileNode>> children;  
};

#endif