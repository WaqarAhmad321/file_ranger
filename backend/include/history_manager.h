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

    void push(const string& path) {
        if (!back_stack.empty() && back_stack.top() == path) {
            return;
        }
        
        back_stack.push(path);
        forward_stack.clear();
    }

    string go_back() {
        if (back_stack.size() <= 1) {
            return "";
        }

        string current = back_stack.top();
        back_stack.pop();
        forward_stack.push(current);

        return back_stack.top();
    }

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
