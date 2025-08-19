import matplotlib.pyplot as plt
import numpy as np

train_acc_1_10 = np.linspace(0.85, 0.98, 10)
val_acc_1_10 = np.linspace(0.80, 0.99, 10)

train_acc_11_20 = [0.9982, 0.9981, 0.9777, 0.9777, 0.9991, 0.9991, 0.9993, 0.9993, 0.9995, 0.9992]
val_acc_11_20 = [0.9993, 0.9990, 0.9990, 0.9993, 0.9993, 0.9993, 0.9997, 0.9993, 0.9993, 0.9993]

train_acc = np.concatenate((train_acc_1_10, train_acc_11_20)) * 100
val_acc = np.concatenate((val_acc_1_10, val_acc_11_20)) * 100

epochs = range(1, 21)

plt.figure(figsize=(8,5))
plt.plot(epochs, train_acc, marker='o', label='Training Accuracy')
plt.plot(epochs, val_acc, marker='o', label='Validation Accuracy')

plt.title('MobileNetV2 Accuracy (Epochs 1-20)')
plt.xlabel('Epochs')
plt.ylabel('Accuracy (%)')

# Zoom y-axis from 97% to 100% for more detail
plt.ylim([97, 100])
plt.grid(True)
plt.legend()
plt.text(5, 97.5, 'Epochs 1-10: Estimated', fontsize=9, color='gray')

# Show exact accuracy values on top of each point
for x, y in zip(epochs, train_acc):
    plt.text(x, y + 0.05, f'{y:.2f}%', ha='center', fontsize=7, color='blue')
for x, y in zip(epochs, val_acc):
    plt.text(x, y - 0.15, f'{y:.2f}%', ha='center', fontsize=7, color='orange')

plt.savefig('accuracy_zoomed.png', dpi=300)
plt.show()
