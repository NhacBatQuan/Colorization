def set_params(params, id_optim):
    if id_optim is None:
        pass
    else:
        if id_optim == 0:
            params.dataset_nsamples = 50000
            params.epochs = 50
            params.seed = 42
            params.batch_size = 32
            params.test_split = 0.2
            params.val_split = 0.4
            params.backbone = 18
            params.dataset = "Colorization/dataset/DatasetTorch/Dataset_150k.csv"
            params.path_nas = "Colorization/"
            params.log_dir = "Debug/"
            params.augmentation = 1
            params.decoder_version = 18
            params.pretrained = 0
            params.input_channels = 9
            params.out_channels = 2
            params.lr = 0.01
            params.optim = "SGD"
            params.img_size = 128     
            params.weight_rec_loss = 100.
            params.grad_loss = 1
            params.weight_grad_loss = 0.1
            params.loss = "L1"
            params.scheduler = 1
            params.sched_step = 40
            params.sched_type = "step"
            params.path_model_dict = "Colorization/" +  params.log_dir + "_batch_torch_quantiles590_decoder18_" + str(params.batch_size) + "_"+ str(params.lr) + "/last.pth.tar"
            params.load_checkpoint = 0
            params.save_checkpoint = 1
            params.dropout = 0.3
            params.num_workers = 0

        params.log_dir = params.log_dir + "_test_compare_2" + str(params.batch_size) + "_" +str(params.lr)

    return params
 