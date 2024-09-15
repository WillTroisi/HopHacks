install.packages("ggplot2")
install.packages("dplyr")
install.packages("devtools")
# setwd("C:\Users\finco\Documents\GitHub\HopHacks")
devtools::install_github("josedv82/bdgramR")

library(bdgramR)
library(ggplot2)
library(dplyr)

df <- read.csv('setVis.csv')

outputFilename <- colnames(df)[1]
colnames(df) <- c("muscleGroup", "sets")
df <- df[-1,]

df <- df %>%
  mutate(muscleGroup = case_when(
    muscleGroup == "neck" ~ "Neck",
    muscleGroup == "forearms" ~ "Forearm",
    muscleGroup == "upper back" ~ "Upper Back",
    muscleGroup == "lower back" ~ "Lower_Back",
    muscleGroup == "glutes" ~ "Gluteus",
    muscleGroup == "hamstrings" ~ "Hamstrings",
    muscleGroup == "quads" ~ "Quadriceps",
    muscleGroup == "calves" ~ "Calves",
    muscleGroup == "pecs" ~ "Pectoral",
    muscleGroup == "abs" ~ "Abdominals",
    muscleGroup == "shoulders" ~ "Arm",
    TRUE ~ muscleGroup
  ))

dat <- bdgramr(data, "original_male")

dat <- dat %>%
  left_join(df, by = c("Group" = "muscleGroup"))



dat$sets <- as.numeric(dat$sets)


plot <- ggplot(dat, aes(x,y, group = Id)) + 
  geom_bdgramr(color = "black", aes(fill = sets)) +
  scale_fill_gradient(low = 'blue', high = 'red')

png(outputFilename)
print(plot)
dev.off()

