#include "GrayScale.h"
#include <vector>
#include <stdexcept>
#include <cmath>

void GrayScale::validateImage(const std::vector<std::vector<std::vector<double>>>& image) {
    if (image.empty()) {
        throw std::invalid_argument("Image is empty");
    }
    
    size_t height = image.size();
    size_t first_width = image[0].size();
    
    for (size_t i = 0; i < height; ++i) {
        if (image[i].size() != first_width) {
            throw std::invalid_argument("All rows must have same width");
        }
        for (size_t j = 0; j < first_width; ++j) {
            if (image[i][j].size() != 3) {
                throw std::invalid_argument("Each pixel must have exactly 3 values (RGB)");
            }
        }
    }
}

std::vector<std::vector<double>> GrayScale::convertToGray(
    const std::vector<std::vector<std::vector<double>>>& rgbImage) {
    
    validateImage(rgbImage);
    
    size_t height = rgbImage.size();
    size_t width = rgbImage[0].size();
    
    std::vector<std::vector<double>> grayImage(height, std::vector<double>(width, 0.0));
    
    const double r_coef = 0.299;
    const double g_coef = 0.587;
    const double b_coef = 0.114;
    
    for (size_t i = 0; i < height; ++i) {
        for (size_t j = 0; j < width; ++j) {
            const auto& pixel = rgbImage[i][j];
            grayImage[i][j] = r_coef * pixel[0] + g_coef * pixel[1] + b_coef * pixel[2];
        }
    }
    
    return grayImage;
}