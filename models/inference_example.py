import torch

# Ejemplo de inferencia con un modelo TorchScript. El modelo devuelve un tensor unidimensional multiplicado por 2. 2
ts = torch.jit.load("./doubleit_model.pt")
sample_tensor = torch.tensor([1, 2, 3, 4])
result = ts(sample_tensor)

print(result)  # <- tensor([2, 4, 6, 8])
