#ifndef CUSTOM_STACK_H
#define CUSTOM_STACK_H

#include <string>
#include <vector>
#include <stdexcept>

using std::string;
using std::vector;

class CustomStack {
private:
    vector<string> data;

public:
    CustomStack() = default;

    void push(const string& value) {
        data.push_back(value);
    }

    void pop() {
        if (!data.empty()) {
            data.pop_back();
        }
    }

    string top() const {
        if (data.empty()) {
            return "";
        }
        return data.back();
    }

    bool empty() const {
        return data.empty();
    }

    size_t size() const {
        return data.size();
    }
    
    void clear() {
        data.clear();
    }
};

#endif
