% cs559_hojustin_project.m
% I pledge my honor that I have abided by the Stevens Honor System.
% Justin Ho

% START: OWN CODE
datapath = "data.csv";       % path to main dataset
extratestpath = "test.csv";  % path to "old" dataset also provided by research team

data = readmatrix(datapath);            % read data into matrix
extra_test = readmatrix(extratestpath); % read extra test data into matrix

fprintf("Random forest classifications of phishing sites\n");
fprintf("==================================================\n");

% to see results after shifting parameter
% (# of trees in random forest)
for numTrees = [1, 5, 10, 25, 50, 80, 100, 200, 500]
    % shift number of iterations
    for iterations = [1, 5, 10]
        fprintf("Number of trees: %d | Number of iterations: %d\n", numTrees, iterations);
        accuracy  = zeros(1, iterations);
        xaccuracy = zeros(1, iterations);
        
        for i=1 : iterations
            % shuffle the dataset
            rand      = randperm(length(data));
            reordered = data(rand, :);
    
            % training and test sets distribute 70:30
            train = data(1:(round(0.7 * length(data))), :);
            test  = data((round(0.7 * length(data)))+1:end, :);
    
            % create random forest using training data
            % column 31 of dataset is class variable
            forest = TreeBagger(numTrees, train, train(:, 31));
    
            % generate random forest predictions for test set
            predicts = predict(forest, test);
            pre_mat  = str2double(predicts);
    
            % compute accuracy of predictions
            [test_correct, test_wrong] = compute_acc(pre_mat, test);
            correct_percent = test_correct / (test_correct + test_wrong);
            accuracy(i) = correct_percent;
    
            % generate random forest predictions for extra test set
            xpredicts = predict(forest, extra_test);
            xpre_mat  = str2double(xpredicts);
    
            % compute accuracy
            [xcorrect, xwrong] = compute_acc(xpre_mat, extra_test);
            xcorrect_percent = xcorrect / (xcorrect + xwrong);
            xaccuracy(i) = xcorrect_percent;
        end
        
        acc_mean  = mean(accuracy);
        acc_std   = std(accuracy);
        xacc_mean = mean(xaccuracy);
        xacc_std  = std(xaccuracy);
        fprintf("Test mean: %f\t\tExtra test mean: %f\n", acc_mean, xacc_mean);
        fprintf("Test std:  %f\t\tExtra test std:  %f\n\n", acc_std, xacc_std);
    end
end

% helper function to calculate corrects and wrongs
function [correct, wrong] = compute_acc(predictions, test)
    [correct, wrong] = deal(0);  % init correct, wrong to 0
    
    for i=1 : length(test)
        if (test(i, 31) == predictions(i))
            correct = correct + 1;
        else
            wrong = wrong + 1;
        end
    end
end
% END: OWN CODE