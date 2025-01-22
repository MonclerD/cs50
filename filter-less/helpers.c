#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average_rgb =
                round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = average_rgb;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaGreen, sepiaRed, sepiaBlue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiaGreen = 0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen +
                         0.168 * image[i][j].rgbtBlue;
            sepiaRed = 0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen +
                       0.189 * image[i][j].rgbtBlue;
            sepiaBlue = 0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen +
                        0.131 * image[i][j].rgbtBlue;

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtGreen = round(sepiaGreen);
            image[i][j].rgbtRed = round(sepiaRed);
            image[i][j].rgbtBlue = round(sepiaBlue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE buffer;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            buffer = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = buffer;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE image_rep[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sum_red = 0, sum_blue = 0, sum_green = 0, total_p = 0;

            for (int updated_i = i - 1; updated_i < i + 2; updated_i++)
            {
                for (int updated_j = j - 1; updated_j < j + 2; updated_j++)
                {
                    if (updated_i >= 0 && updated_j >= 0 && updated_i < height && updated_j < width)
                    {
                        sum_red += image[updated_i][updated_j].rgbtRed;
                        sum_blue += image[updated_i][updated_j].rgbtBlue;
                        sum_green += image[updated_i][updated_j].rgbtGreen;
                        total_p++;
                    }
                }
            }
            image_rep[i][j].rgbtRed = round(sum_red / total_p);
            image_rep[i][j].rgbtBlue = round(sum_blue / total_p);
            image_rep[i][j].rgbtGreen = round(sum_green / total_p);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = image_rep[i][j];
        }
    }
    return;
}
