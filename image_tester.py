import image_comparison

blah = imageCompare.ImageCompareSSIM(r"images\1.jpg", r"images\2.jpg")
var = blah.compare_value
print(var)

blah = imageCompare.ImageCompareSSIM(r"images\1.jpg", r"images\2.jpg", False)
var = blah.compare_value
print(var)

blah = imageCompare.ImageCompareSSIM(r"images\1.jpg", r"images\2.jpg", True, 500, 500)
var = blah.compare_value
print(var)