import pandas as pd

from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.saving.save import load_model

from app.MainApp import MainApp
from models.VGG16 import VGG16
from models.AlexNet import AlexNet
from PokeDex.PokeDex import PokeDex


def main():
    model_type = 'VGG16'  # Options include AlexNet or VGG16
    train = False  # True if training new model, False if launching application

    # Define final variables
    data_dir = '/Users/handw/Desktop/pkmn'
    pokemon_dir = '/Users/handw/PycharmProjects/PIKA/'
    pokedex_dir = pokemon_dir + 'PokeDex/images/'
    saved_model_dir = pokemon_dir + 'models/saved/AlexNet/model_epoch_255' if model_type == 'AlexNet' \
        else pokemon_dir + 'models/saved/VGG16/model_epoch_122'

    # Create target_size based on model_type chosen
    target_size = (277, 277) if model_type == 'AlexNet' else (224, 224)
    epochs = 300
    batch_size = 50

    model = None

    # Initialize PokeDex in English
    pokedex = PokeDex('en')

    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True,
                                       validation_split=0.2)  # set validation split

    train_gen = train_datagen.flow_from_directory(
        data_dir,
        target_size=target_size,
        batch_size=batch_size,
        subset='training')  # set as training data

    test_gen = train_datagen.flow_from_directory(
        data_dir,  # same directory as training data
        target_size=target_size,
        batch_size=batch_size,
        subset='validation')  # set as validation data

    label_dict = train_gen.class_indices

    if model_type == 'AlexNet':
        model = AlexNet(train_gen, test_gen, epochs=epochs, batch_size=batch_size)
    elif model_type == 'VGG16':
        model = VGG16(train_gen, test_gen, epochs=epochs, batch_size=batch_size)

    print("Finished initializing model")

    if train:
        model.train()
    else:
        loaded_model = load_model(saved_model_dir)

        df = pd.read_csv(pokemon_dir + 'PokeDex/Pokemon Info.csv', encoding="ISO-8859-1")

        app = MainApp(loaded_model, df, pokedex, pokedex_dir, label_dict, train_gen.num_classes, target_size)
        app.run()


main()
