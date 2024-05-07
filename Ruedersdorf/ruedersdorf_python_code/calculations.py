# pixel_to_degree_mapping = {
#     135: 360, 133: 350, 131: 340, 129: 330, 126: 320, 123: 310, 119: 300, 118: 290,
#     111: 280, 107: 270, 102: 260, 100: 250, 97: 240, 90: 230, 88: 220, 82: 210,
#     77: 200, 73: 190, 69: 180, 67: 170, 64: 160, 61: 150, 58: 140, 54: 130,
#     50: 120, 48: 110, 42: 100, 38: 90, 34: 80, 30: 70, 27: 60, 23: 50,
#     18: 40, 14: 30, 9: 20, 6: 10
# }

import asyncio


pixel_to_degree_mapping = {
    176:0,176:10,296:20,455:30,604:40,727:50,881:60,986:70,1103:80,1212:90,1301:100,1437:110,1578:120,1714:130,1826:140,1906:150,2008:160,2105:170,2203:180,2294:190,
    2411:200,2578:210,2719:220,2836:230,3032:240,3129:250,3192:260,3310:270,3420:280,3551:290,3649:300,3825:310,3920:320,3997:330,4068:340,4164:350
}


async def calculate_angle(pixel_value):
    # Find the nearest two pixel values in the reverse mapping
    nearest_pixels = sorted(
        pixel_to_degree_mapping.keys(), key=lambda x: abs(x - pixel_value))[:2]

    # Calculate the average of the corresponding degrees based on pixel value differences
    pixel_difference1 = abs(nearest_pixels[0] - pixel_value)
    pixel_difference2 = abs(nearest_pixels[1] - pixel_value)

    weight1 = pixel_difference2 / (pixel_difference1 + pixel_difference2)
    weight2 = pixel_difference1 / (pixel_difference1 + pixel_difference2)

    degree_average = weight1 * pixel_to_degree_mapping[nearest_pixels[0]] + \
        weight2 * pixel_to_degree_mapping[nearest_pixels[1]]

    return degree_average



# async def main():
#     print(await calculate_angle(1600))

# asyncio.run(main())