#include <cs50.h>
#include <stdio.h>

void print_row(int spaces, int bricks);

int main(void)
{

    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    // Print a pyramid of that height
    for (int i = 0; i < n; i++)
    {
        int spaces = n - i - 1;
        int bricks = i + 1;

        print_row(spaces, bricks);
    }
}

void print_row(int spaces, int bricks)
{
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }

    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }

    printf("  ");

    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }
    printf("\n");
}
