This is a DCGAN project on the LSUN dataset. 
the code will fully automate the dataflow pipeline 
which includes downloading the data into my google colab instance, 
extracting the zip files, exporting the images from the downloaded database,
reading every image and storing the pixel values as a numpy array, 
storing the numpy array as a .npy file,
reading the .npy file and training the DCGAN model on it.

There are different datasets of very different sizes.
I used the "church_outdoor_train_lmdb" dataset which is just 2GB 
but took 12 hours to train.

If you want to train on a different dataset, then just change the 
file name and the code will do the rest automatically.
