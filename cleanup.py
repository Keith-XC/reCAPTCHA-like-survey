import os, shutil

model = 'LQ'

model_folder = os.path.join('./img', model)
for class_folder in os.listdir(model_folder):
  class_path = os.path.join(model_folder, class_folder)
  if os.path.isdir(class_path):
    for seed in os.listdir(class_path):
      seed_path = os.path.join(class_path, seed)
      if os.path.isdir(seed_path):
        for style in os.listdir(seed_path):
          style_path = os.path.join(seed_path, style)
          if os.path.isdir(style_path):
            print(style_path)
            shutil.rmtree(style_path)