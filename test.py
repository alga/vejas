from gfs import WindPicture
from gfs import PrecipitationPicture
from gfs import TempPicture

#pic = WindPicture(file="/home/alga/Rtavn009.png")
#pic.compose().show()
#pic.getFullScale().show()

#pic = PrecipitationPicture(file="/home/alga/Rtavn064.png")
#pic.compose().show()
#pic.getFullScale().show()

pic = TempPicture("06")
pic.compose().show()
pic.getFullScale().show()
