import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np

saved_model = tf.keras.models.load_model("minist_h5_model.h5")

def prepare_data_set():
    (ds_train, ds_test), ds_info = tfds.load(
        'mnist',
        split=['train', 'test'],
        shuffle_files=True,
        as_supervised=True,
        with_info=True,
    )

    def normalize_img(image, label):
        """Normalizes images: `uint8` -> `float32`."""
        return tf.cast(image, tf.float32) / 255., label

    ds_train = ds_train.map(
        normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds_train = ds_train.cache()
    ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
    ds_train = ds_train.batch(128)
    ds_train = ds_train.prefetch(tf.data.experimental.AUTOTUNE)

    ds_test = ds_test.map(
        normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds_test = ds_test.batch(128)
    ds_test = ds_test.cache()
    ds_test = ds_test.prefetch(tf.data.experimental.AUTOTUNE)
    return ds_test, ds_train


# tf.enable_v2_behavior()
def train():
    ds_test, ds_train = prepare_data_set()
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    model.fit(
        ds_train,
        epochs=6,
        validation_data=ds_test,
    )
    print("Saving model")
    model.save("minist_h5_model.h5")


def test():
    saved_model = tf.keras.models.load_model("minist_h5_model.h5")
    print(saved_model)
    print(saved_model.summary())

    (ds_train, ds_test), ds_info = tfds.load(
        'mnist',
        split=['train', 'test'],
        shuffle_files=True,
        as_supervised=True,
        with_info=True,
    )

    print(ds_test)
    iterator = ds_train.__iter__()
    next_element = iterator.get_next()
    print(next_element[1])
    label = next_element[1].numpy()
    image = next_element[0]
    image = image.numpy()

    image = np.reshape(image, (28, 28))
    plt.imshow(image)
    image = tf.cast(image, tf.float32) / 255.
    predicted_label = saved_model.predict(image)
    print(f"{label=},{predicted_label}")


def predict(image):
    from PIL import Image
    image = Image.open(image)
    image = image.resize((28, 28))
    image_array = np.asarray(image)
    img_gray = image_array[:, :, 0]
    img = tf.cast(img_gray, tf.float32) / 255.0
    img = tf.reshape(img, (-1, 28, 28))
    result = saved_model.predict(img)
    ##
    label = np.argmax(result)
    return label


