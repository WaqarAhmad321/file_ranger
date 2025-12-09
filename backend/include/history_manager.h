#ifndef HISTORY_MANAGER_H
#define HISTORY_MANAGER_H

#include "custom_stack.h"
#include <string>

using std::string;

class HistoryManager {
private:
    CustomStack back_stack;
    CustomStack forward_stack;

public:
    HistoryManager() = default;

    // Initialize with the starting path
    void init(const string& path) {
        back_stack.clear();
        forward_stack.clear();
        back_stack.push(path);
    }

    // Navigate to a new path
    void push(const string& path) {
        // If we are already at this path (top of back stack), do nothing
        if (!back_stack.empty() && back_stack.top() == path) {
            return;
        }
        
        back_stack.push(path);
        // When we manually navigate, forward history is cleared
        forward_stack.clear();
    }

    // Go back: returns the previous path, or empty string if no history
    string go_back() {
        if (back_stack.size() <= 1) {
            return ""; // Cannot go back further than start
        }

        string current = back_stack.top();
        back_stack.pop();
        forward_stack.push(current);

        return back_stack.top();
    }

    // Go forward: returns the next path, or empty string if no history
    string go_forward() {
        if (forward_stack.empty()) {
            return "";
        }

        string next = forward_stack.top();
        forward_stack.pop();
        back_stack.push(next);

        return next;
    }
    
    string current() {
        return back_stack.top();
    }
};

#endif
