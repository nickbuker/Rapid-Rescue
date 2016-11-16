library(plyr)

model_data <- read.csv("~/Documents/DSI/DSI_capstone/data/model_data_no_out.csv")

model_data_counted = count(model_data, vars = c('mariners_home',
                                                'seahawks_home',
                                                'sounders_home',
                                                'trav_holiday',
                                                'dang_holiday', 
                                                'night',
                                                'Monday',
                                                'Saturday',
                                                'Sunday',
                                                'Thursday',
                                                'Tuesday',
                                                'Wednesday',
                                                'day_num',
                                                'zone1',
                                                'zone2',
                                                'zone3',
                                                'zone4',
                                                'zone5',
                                                'zone6',
                                                'zone7',
                                                'seasonality'))

write.csv(model_data_counted, file = 'model_data_counted_no_out.csv')
