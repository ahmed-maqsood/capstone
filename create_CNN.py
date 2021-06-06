from pathlib import Path
from tensorflow import keras
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

def process(image_file, label):
    image_file = tf.cast(image_file/255, tf.float32)
    return image_file, label

# Transfer learning but feature learning layers are also being trained to have their weights adjusted
def generate_model_TF_fine_tune():
    base_model = keras.applications.MobileNet(
        weights="imagenet",
        input_shape=(224, 224, 3),
        include_top=False)

    base_model.trainable = False

    inputs = keras.Input(shape=(224, 224, 3))

    x = base_model(inputs, training=False)
    x = keras.layers.GlobalAveragePooling2D()(x)

    outputs = keras.layers.Dense(4, activation="softmax")(x)
    model = keras.Model(inputs, outputs)

    return model, base_model


def main():

    training_data = tf.keras.preprocessing.image_dataset_from_directory("data_set/",
                                                                        image_size=(224, 224),
                                                                        label_mode="categorical",
                                                                        shuffle=True,
                                                                        class_names=["normal_images",
                                                                                     "under_extruded_images",
                                                                                     "over_extruded_images",
                                                                                     "no_pattern"])

    training_data = training_data.map(process)


    model, base_model = generate_model_TF_fine_tune()
    base_model.trainable = True
    model_name = base_model.name

    # Compile the Model
    model.compile(loss="categorical_crossentropy",
                  optimizer=keras.optimizers.Adam(1e-5),
                  metrics=["accuracy"])

    # Print a summary of model
    # Note, Param # means total number of weights in that layer
    model.summary()

    # Train the model
    model.fit(
        training_data,
        epochs=10
    )

    # Save neural network structure
    model_structure = model.to_json()
    file_path = Path(f"model_{model_name}_structure.json")
    file_path.write_text(model_structure)

    # Save neural network's trained weights
    model.save_weights(f"model_{model_name}_weights.h5")


if __name__ == '__main__':
    main()
