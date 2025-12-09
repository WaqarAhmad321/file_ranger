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
    }
    // Sort children before returning (directories first, then case-insensitive by name)
    try {
        // comparator: directories first, then case-insensitive name
        auto cmp = [](const shared_ptr<FileNode>& a, const shared_ptr<FileNode>& b) {
            if (a->is_directory != b->is_directory) return a->is_directory && !b->is_directory;
            // case-insensitive compare
            auto to_lower = [](const string& s) {
                string out; out.reserve(s.size());
                for (unsigned char c: s) out.push_back(std::tolower(c));
                return out;
            };
            return to_lower(a->name) < to_lower(b->name);
        };

        std::sort(node->children.begin(), node->children.end(), cmp);
    } catch (const std::exception&) {
        // ignore sort errors
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
