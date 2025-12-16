#include "../include/file_node.h"
#include <filesystem>
#include <algorithm>
#include <cctype>
#include <system_error>
#include <fstream>

namespace fs = std::filesystem;
using fs::path;
using fs::directory_iterator;
using fs::is_directory;
using std::string;
using std::cout;
using std::endl;
using std::unique_ptr;
using std::shared_ptr;
using std::make_shared;

// -------------------------
// Manual Merge Sort Implementation
// -------------------------

// Helper function to convert string to lowercase for case-insensitive comparison
string to_lower(const string& s) {
    string result;
    result.reserve(s.size());
    for (unsigned char c : s) {
        result.push_back(std::tolower(c));
    }
    return result;
}

// Comparator function: directories first, then case-insensitive alphabetical
bool compare_nodes(const shared_ptr<FileNode>& a, const shared_ptr<FileNode>& b) {
    // Primary criterion: directories before files
    if (a->is_directory != b->is_directory) {
        return a->is_directory && !b->is_directory;
    }
    // Secondary criterion: case-insensitive name comparison
    return to_lower(a->name) < to_lower(b->name);
}

// Merge function: merges two sorted halves
void merge(vector<shared_ptr<FileNode>>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    // Create temporary vectors
    vector<shared_ptr<FileNode>> leftArr(n1);
    vector<shared_ptr<FileNode>> rightArr(n2);

    // Copy data to temporary vectors
    for (int i = 0; i < n1; i++) {
        leftArr[i] = arr[left + i];
    }
    for (int j = 0; j < n2; j++) {
        rightArr[j] = arr[mid + 1 + j];
    }

    // Merge the temporary vectors back into arr[left..right]
    int i = 0;    // Initial index of left subarray
    int j = 0;    // Initial index of right subarray
    int k = left; // Initial index of merged subarray

    while (i < n1 && j < n2) {
        if (compare_nodes(leftArr[i], rightArr[j])) {
            arr[k] = leftArr[i];
            i++;
        } else {
            arr[k] = rightArr[j];
            j++;
        }
        k++;
    }

    // Copy remaining elements of leftArr[], if any
    while (i < n1) {
        arr[k] = leftArr[i];
        i++;
        k++;
    }

    // Copy remaining elements of rightArr[], if any
    while (j < n2) {
        arr[k] = rightArr[j];
        j++;
        k++;
    }
}

// Merge Sort function (recursive)
void merge_sort(vector<shared_ptr<FileNode>>& arr, int left, int right) {
    if (left < right) {
        // Find the middle point
        int mid = left + (right - left) / 2;

        // Recursively sort first and second halves
        merge_sort(arr, left, mid);
        merge_sort(arr, mid + 1, right);

        // Merge the sorted halves
        merge(arr, left, mid, right);
    }
}

// Wrapper function to call merge sort
void sort_file_nodes(vector<shared_ptr<FileNode>>& nodes) {
    if (nodes.size() > 1) {
        merge_sort(nodes, 0, nodes.size() - 1);
    }
}

// -------------------------
// Directory Listing
// -------------------------

shared_ptr<FileNode> list_directory(const string& dir_path) {
    auto node = make_shared<FileNode>();
    node->name = path(dir_path).filename().string();
    node->path = dir_path;
    node->is_directory = is_directory(dir_path);
    node->size = 0;

    if (node->is_directory) {
        for (const auto& entry : directory_iterator(dir_path)) {
            auto child_node = make_shared<FileNode>();
            child_node->name = entry.path().filename().string();
            child_node->path = entry.path().string();
            child_node->is_directory = is_directory(entry.path());

             // Safely get file size
            try {
                child_node->size = (entry.is_regular_file()) ? entry.file_size() : 0;
            } catch (...) {
                child_node->size = 0;
            }

            node->children.push_back(child_node);
        }
        
        // Sort children using manual merge sort implementation
        sort_file_nodes(node->children);
    }

    return node; // directly return the shared_ptr
}

// -------------------------
// File operations (used by Python UI)
// -------------------------

bool make_directory_recursive(const string& dir_path) {
    try {
        return std::filesystem::create_directories(dir_path);
    } catch (const std::filesystem::filesystem_error&) {
        return false;
    }
}

bool remove_path_recursive(const string& target_path) {
    try {
        std::error_code ec;
        std::uintmax_t removed = std::filesystem::remove_all(target_path, ec);
        return ec ? false : (removed > 0);
    } catch (...) {
        return false;
    }
}

bool rename_path(const string& oldp, const string& newp) {
    try {
        std::error_code ec;
        std::filesystem::rename(oldp, newp, ec);
        return !ec;
    } catch (...) {
        return false;
    }
}

bool copy_path(const string& src, const string& dest) {
    try {
        std::error_code ec;
        std::filesystem::copy(src, dest, std::filesystem::copy_options::recursive | std::filesystem::copy_options::overwrite_existing, ec);
        return !ec;
    } catch (...) {
        return false;
    }
}

bool touch_file(const string& file_path) {
    try {
        std::ofstream ofs(file_path, std::ios::app);
        return ofs.good();
    } catch (...) {
        return false;
    }
}
