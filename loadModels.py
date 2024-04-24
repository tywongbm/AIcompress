from model import *

def train(latent_dim):
    
    CHECKPOINT_PATH = 'lossless\AE\saved_models'  
    model_checkpoint = ModelCheckpoint(
        dirpath=os.path.join(CHECKPOINT_PATH),
        filename=f"cifar10_{latent_dim}",
        save_on_train_epoch_end=True,
        save_weights_only=True
    )
    # Create PyTorch Lightning trainer 
    trainer = pl.Trainer(default_root_dir=os.path.join(CHECKPOINT_PATH, f"cifar10_{latent_dim}"),
                         accelerator="gpu" if str(device).startswith("cuda") else "cpu",
                         #accelerator="cpu",
                         devices=1,
                         max_epochs=100,
                         callbacks=[Callback(get_train_images(8), every_n_epochs=10),
                                    LearningRateMonitor("epoch")])

    # Check whether pretrained model exists
    pretrained_filename = os.path.join(CHECKPOINT_PATH, f"cifar10_{latent_dim}.ckpt")
    if os.path.isfile(pretrained_filename):
        print("Found pretrained model, loading...")
        model = AE.load_from_checkpoint(pretrained_filename)
    else:
        model = AE(num_input_channels=3,base_channel_size=32, latent_dim=latent_dim)
        trainer.fit(model, train_loader, val_loader)
        #save model weights at "cifar10_{latent_dim}"
        trainer.save_checkpoint(pretrained_filename)
        
    val_result = trainer.test(model, val_loader, verbose=False)
    test_result = trainer.test(model, test_loader, verbose=False)
    result = {"test": test_result, "val": val_result}
    return model, result

model_dict = {}
for latent_dim in [64, 128, 256, 384, 512, 768, 1024, 1240, 1512, 2048]:
    model_ld = train(latent_dim)
    model_dict[latent_dim] = {"model": model_ld}

# model = AE.load_from_checkpoint('lossless/AE/saved_models/cifar10_64.ckpt')
#print(model_dict)


def plot_reconstructions(model, input_imgs):
    # Reconstruct images
    model.eval()
    with torch.no_grad():
        reconst_imgs = model(input_imgs.to(model.device))
    reconst_imgs = reconst_imgs.cpu()
    

    # Calculate reconstruction error
    loss = F.mse_loss(input_imgs, reconst_imgs, reduction="none") / 8
    loss = loss.sum(dim=[1,2,3]).mean(dim=[0]).item()
    
    # Plotting
    imgs = torch.stack([input_imgs, reconst_imgs], dim=1).flatten(0,1)
    grid = torchvision.utils.make_grid(imgs, nrow=4, normalize=True, range=(-1,1))
    grid = grid.permute(1, 2, 0)
    plt.figure(figsize=(7,4.5))
    plt.title(f"Reconstructed from {model.hparams.latent_dim} latents with averaged loss {loss:.2f}")
    plt.imshow(grid)
    plt.axis('off')
    plt.show()

input_imgs = get_train_images(8)
for latent_dim in model_dict:
    plot_reconstructions(model_dict[latent_dim]["model"], input_imgs)

# #show lena.jpeg AND convert to torch tensor in (1,3,32,32) shape
# from PIL import Image
# import torch
# import numpy as np
# img = Image.open("lossless/AE/lena.jpeg")
# img = img.resize((32,32))
# img = np.array(img)
# plt.imshow(img)
# plt.axis('off')
# plt.show()
# img = img.transpose(2,0,1)
# img = torch.tensor(img).float()
# img = img.unsqueeze(0)
# img = img/255
# img = (img-0.5)/0.5
# img.shape

# for latent_dim in model_dict:
#     plot_reconstructions(model_dict[latent_dim]["model"], img)