```
loss "categorical_crossentropy"
metric "accuracy"
```


# model1:
2 convolution(64,(3,3)) + max-pooling(2,2) layers

1 convolution(64,(3,3)) layer

1 input layer Flatten()

1 dense hidden layer 128 units activation = Relu with dropout 0.25

1 output layer with softmax

optimizer "adam"

10 EPOCHS


### result:

training set:  96.42%

validation set:  95.81%

> after seeing the results which are good but can be better i decided to add and extra hidden layer same size but no dropout also i changed the kernel size for the last convolution layer to 5 x 5

# model2:
2 convolution(64,(3,3)) + max-pooling(2,2) layers

1 convolution(32,(5,5)) layer

1 input layer Flatten()

1 dense hidden layer 128 units activation = Relu with dropout 0.25

1 dense hidden layer 128 units activation = Relu 

1 output layer with softmax

optimizer "adam"

10 EPOCHS

### result:

training set:  5.52%

validation set:  5.84%

> for some reason this model performed really poorly but i wasn't sure whether it was because of the new hidden layer or because of the new kernel size so i decided to test and see which one was the one the messes up with the model...

> so first i will remove the hideen layer and keep the new kernel size...


# model3:
2 convolution(64,(3,3)) + max-pooling(2,2) layers

1 convolution(32,(5,5)) layer

1 input layer Flatten()

1 dense hidden layer 128 units activation = Relu with dropout 0.25

1 output layer with softmax

optimizer "adam"

10 EPOCHS

### result:
training set:  5.39%

validation set:  5.51%

> well apearently that didn't really help and this means that the probelem is probably within the new kernel size either it is because it captures some features to the point were it is not helpful or something else idk...

> for that reason lets readd the hidden layer and change the kernel size back to the original one

# model4:
2 convolution(64,(3,3)) + max-pooling(2,2) layers

1 convolution(64,(3,3)) layer

1 input layer Flatten()

1 dense hidden layer 128 units activation = Relu with dropout 0.25

1 dense hidden layer 128 units activation = Relu 

1 output layer with softmax

optimizer "adam"

10 EPOCHS

### result:
training set:  95.8%

validation set:  97.08%

> ok much better. this means that there was appearently some problem with using a bigger kernel size for the convolution

> next i want to turn my attention to the pooling aspect of image processing

> so first i added a final pooling layer before entering the neural network also i changed all the pools from max-pooling to average pooling because i want to see whether that changes anything or it doesn't really matter for this dataset ?

# model5:
3 convolution(64,(3,3)) + average-pooling(2,2) layers
1 input layer Flatten()
1 dense hidden layer 128 units activation = Relu with dropout 0.25
1 dense hidden layer 128 units activation = Relu 
1 output layer with softmax
optimizer "adam"
loss "categorical_crossentropy"
10 EPOCHS

### result:
training set:  96.22%

validation set:  96.88%

> well that turned out not to be that important judging by the results they look pretty similar...

> lets try another thing...

> i think we can try and play with the optimizer...  now as far as i understand and optimizer is how we calculate the gradient and nudge the weight values to try and find a local minima this is related to learning rate and it is also related to add some additional randomness to the algorithm in order to find better solutions

> so far we have been using adaptime moment estimation(adam) which is and extended version of Stochastic Gradient Decent(SGD) but i wonder whether this enhanced algorithm really matters in our case or not ?

> i will stick with all of the previous setup except for the optimizer i will change to SGD



# model6:
3 convolution(64,(3,3)) + average-pooling(2,2) layers

1 input layer Flatten()

1 dense hidden layer 128 units activation = Relu with dropout 0.25

1 dense hidden layer 128 units activation = Relu 

1 output layer with softmax

optimizer "SGD"

10 EPOCHS

### result:
training set:  91.55%

validation set:  95.15%

> now that is a significant degradation in terms of accuracy but i noticed while training the network that it kind of steadily increases so i wonder whether increasing the number of EPOCHS would help or not

> again same setup but i will set EPOCHS to 20


# model7:
3 convolution(64,(3,3)) + average-pooling(2,2) layers

1 input layer Flatten()

1 dense hidden layer 128 units activation = Relu with dropout 0.25

1 dense hidden layer 128 units activation = Relu 

1 output layer with softmax

optimizer "SGD"

20 EPOCHS

### result:
training set:  97.57%

validation set:  97.47%

> well that certainly helped it seems like performs as well as adam when increasing the EPOCH number...  but i wonder what if we increase the EPOCH number while using adam would that help or would it stay almost the same after converging to a certain value

> again same setup just changing optimizer back to "adam"


# model8:
3 convolution(64,(3,3)) + average-pooling(2,2) layers

1 input layer Flatten()

1 dense hidden layer 128 units activation = Relu with dropout 0.25

1 dense hidden layer 128 units activation = Relu 

1 output layer with softmax

optimizer "adam"

20 EPOCHS

### result:
training set:  98.27%

validation set:  98.37%


> well this seems like the best result so far !!

> though i still wonder what is the effect of dropout on the quality of our neural network and whether that will change the accuracy a lot or will it have a minor impact ?

>  again same setup i will only change dropout from 0.25 to 0.35 and see what happens.


# model9:
3 convolution(64,(3,3)) + average-pooling(2,2) layers

1 input layer Flatten()

1 dense hidden layer 128 units activation = Relu with dropout 0.35

1 dense hidden layer 128 units activation = Relu 

1 output layer with softmax

optimizer "adam"

20 EPOCHS

### result:
training set:  97.67%

validation set:  97.71%


> well it seems like it didn't matter that much !!

> now this is my final model and the one i will be submitting

> i will turn the dropout back to 0.25 i will use "adam" and i will stick with average pooling but i will reset the EPOCH number back to 10



# model10:
3 convolution(64,(3,3)) + average-pooling(2,2) layers

1 input layer Flatten()

1 dense hidden layer 128 units activation = Relu with dropout 0.25

1 dense hidden layer 128 units activation = Relu 

1 output layer with softmax

optimizer "adam"

10 EPOCHS

### result:
training set:  96.95%

validation set:  97.60%


# final conclusions
* it seems like adam find a solution faster than SGD and we need to increase the batch number for SGD to catch up
* it seems like there is not difference between max-pooling and average pooling especially in our case
* it seems like having a bigger kernel size for the convolution layer makes it harder to capture some the more important features of the images and actually messes up the model
* it seems like dropout change the accuarcy of the model but slightly but because of it we were able to avoid overfitting
* i would like to experiment with different pool sizes and different actiavtion and loss functions in the future hopefully i will do that soon...
