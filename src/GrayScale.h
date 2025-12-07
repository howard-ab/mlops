#pragma once
#include <vector>
#include <stdexcept>

class GrayScale {
public:
    static std::vector<std::vector<double>> convertToGray(
        const std::vector<std::vector<std::vector<double>>>& rgbImage);
    
private:
    static void validateImage(const std::vector<std::vector<std::vector<double>>>& image);
};