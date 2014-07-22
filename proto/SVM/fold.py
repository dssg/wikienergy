#Accepts X and y and returns a list of training x and a test x and a training y and a validate y
def folds(x_one,x_two,size):
    ####hhhhhmmmmmmmmmm
    train_x = []
    train_y = []
    predict_x = []
    validate_y = []
    cut_index_one = int(len(x_one)/float(size))
    cut_index_two = int(len(x_two)/float(size))
    for i in range(size):
        predict_cut,validate_cut,train_cut_x,train_cut_y = ([] for i in range(4))
        cut_index_start_one = i*cut_index_one
        cut_index_end_one = (i+1)*cut_index_one
        cut_index_start_two = i*cut_index_two
        cut_index_end_two = (i+1)*cut_index_two
        predict_cut.extend(x_one[cut_index_start_one:cut_index_end_one])
        [validate_cut.append(-1) for i in x_one[cut_index_start_one:cut_index_end_one]]
        predict_cut.extend(x_two[cut_index_start_two:cut_index_end_two])
        [validate_cut.append(1) for i in x_two[cut_index_start_two:cut_index_end_two]]
        train_cut_x.extend(x_one[0:cut_index_start_one])
        train_cut_x.extend(x_one[cut_index_end_one:len(x_one)])
        [train_cut_y.append(-1) for i in range(len(x_one)-cut_index_one)]
        train_cut_x.extend(x_two[0:cut_index_start_two])
        train_cut_x.extend(x_two[cut_index_end_two:len(x_two)])
        [train_cut_y.append(1) for i in range(len(x_two)-cut_index_two)]
        train_x.append(train_cut_x)
        train_y.append(train_cut_y)
        predict_x.append(predict_cut)
        validate_y.append(validate_cut)
    return train_x, train_y, predict_x, validate_y



