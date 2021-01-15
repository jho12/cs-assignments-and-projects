data = readmatrix('pima-indians-diabetes.csv');  % read data into matrix
accuracy   = [];  % records accuracy of each iteration
iterations = 10;  % number of iterations

% for each iteration:
for i = 1 : iterations
    % shuffle the dataset
    rand      = randperm(length(data));
    reordered = data(rand, :);
    
    % computer mle of shuffled dataset;
    % return number of correct and wrong determinations
    [correct, wrong] = compute_mle(reordered);
    correct_percent  = correct / (correct + wrong);
    
    % calculate accuracy and record
    accuracy = [accuracy correct_percent];
end

%record overall mean and std. dev.
acc_mean = mean(accuracy);
acc_std  = std(accuracy);

fprintf("Accuracy of MLE, iterated on %d times:\n", iterations);
fprintf("Mean: %f\n", acc_mean);
fprintf("Standard deviation: %f\n", acc_std);
disp("Array of percentages of correctness");
disp(accuracy);

% helper function that computes number of corrects and wrongs
function [correct, wrong] = compute_mle(data)
    % training and test sets each take half of the dataset
    train = data(1:length(data)/2, :);
    test  = data((length(data)/2)+1:end, :);
    
    feats = [2:4];  % features to train on
    
    % calculate means on training data of class variable
    mu_1  = mean(train(train(:, 9) == 0, feats));
    mu_2  = mean(train(train(:, 9) == 1, feats));
    
    % calculate covariance matrices
    % on training data of class variable
    cov_1 = cov(train(train(:, 9) == 0, feats));
    cov_2 = cov(train(train(:, 9) == 1, feats));
    
    % calculate priors on class variables
    len_1 = length(train(train(:, 9) == 0));
    len_2 = length(train(train(:, 9) == 1));
    pri_1 = len_1 / (len_1 + len_2);
    pri_2 = len_2 / (len_1 + len_2);
    
    [correct, wrong] = deal(0);  % initialize correct and wrong
    
    % for each element in test set:
    for i=1 : length(test)
        % calculate likelihoods on class variables
        lik_1 = exp(-(1/2) * (test(i, feats) - mu_1) / cov_1 * transpose(test(i, feats) - mu_1)) / ((2 * pi)^(length(test) / 2) * sqrt(det(cov_1)));
        lik_2 = exp(-(1/2) * (test(i, feats) - mu_2) / cov_2 * transpose(test(i, feats) - mu_2)) / ((2 * pi)^(length(test) / 2) * sqrt(det(cov_2)));
        
        % calculate posteriors on class variables
        pst_1 = lik_1 * pri_1;
        pst_2 = lik_2 * pri_2;
        
        % test if determination is correct
        if (pst_1 > pst_2 && test(i, 9) == 0)
            correct = correct + 1;
        elseif (pst_1 < pst_2 && test(i, 9) == 1)
            correct = correct + 1;
        else
            wrong = wrong + 1;
        end
    end
end