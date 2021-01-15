data = readmatrix('pima-indians-diabetes.csv');  % read data into matrix
accuracy   = [];  % records accuracy of each iteration
means      = [];  % records overall means for each k
stds       = [];  % records overall std. dev. for each k
iterations = 10;  % number of iterations on each k

fprintf("Accuracy of KNN, iterated on %d times each\n\n", iterations);

% for each k:
for k = [1 5 11]
    % for each iteration:
    for i=1 : iterations
        % shuffle the dataset
        rand      = randperm(length(data));
        reordered = data(rand, :);
        
        % compute knn of shuffled dataset;
        % return number of correct and wrong determinations
        [correct, wrong] = compute_knn(reordered, k);
        
        % calculate accuracy and record
        correct_percent  = correct / (correct + wrong);
        accuracy = [accuracy correct_percent];
        acc_mean = mean(accuracy);
        acc_std  = std(accuracy);
    end
    
    % record overall means and stds
    means = [means acc_mean];
    stds  = [stds acc_std];
    
    fprintf("k = %d\n", k);
    fprintf("Mean: %f\n", acc_mean);
    fprintf("Standard deviation: %f\n", acc_std);
    disp("Array of percentages of correctness");
    disp(accuracy);
    
    accuracy = [];  % clear accuracy array
end

% helper function that computes number of corrects and wrongs
function [correct, wrong] = compute_knn(data, k)
    % training and test sets each take half of the dataset
    train = data(1:(length(data) / 2), :);
    test  = data((length(data) / 2)+1:end, :);
    
    feats = [2:4];               % features to train on
    [correct, wrong] = deal(0);  % initialize correct and wrong
    
    % for each element in test set:
    for i=1 : length(test)
        % find the indices of k nearest neighbors to test[i]
        indices   = knnsearch(train(:, feats), test(i, feats), 'K', k);
        
        % the k nearest neighbors
        neighbors = train(indices, :);
        
        % calculate if the neighbors determines if
        % test[i] has diabetes
        class_sum = sum(neighbors(:, 9));
        has_diabetes = round(class_sum / k);
    
        % test if the determination is correct
        if (test(i, 9) == has_diabetes)
            correct = correct + 1;
        else
            wrong = wrong + 1;
        end
    end
end