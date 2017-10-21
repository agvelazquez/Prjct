clc;
clear all;
close all;
%% Data
X_train = csvread('X_train.csv');
X_test = csvread('X_test.csv');
y_train = csvread('y_train.csv');
y_test = csvread('y_test.csv');
index = (1:1:length(y_test))';
y_test = [y_test(:,1),y_test(:,2),index];
TrainingSET = [y_train,X_train];
TestSET = [y_test,X_test];


%% Hyperparameters 
p = [0.01,0.02,0.1,0.3,0.5,0.8];            %epsilon
c = [100,1000,5000,10000,25000];  %cost [2^-3:2^3:2^15]; 
g = [0.01,0.1,0.8,2,3,5,8];             %gamma
%% Model Training
folds = 5;
best_MSE = 100; 
for i = 1:numel(p)
    for j = 1:numel(c)
        for k = 1:numel(g)
        model = svmtrain(y_train(:,2),X_train(:,2),...
        sprintf ('-s 3 -t 2 -c %f -p %f -v %d -g %f -q', c(j), p(i), folds, g(k)));
             if model < best_MSE
                best_MSE = model;
                best_cost    = c(j);
                best_epsilon = p(i);
                best_gamma   = g(k);
             end
        end
    end
end

%% Testing phase
finalmodel= svmtrain(y_train(:,2),X_train(:,2),...
            sprintf ('-c %f -p %f -g %f -s 3 -t 2 -q', best_cost, best_epsilon, best_gamma));
[predicted_value,accuracy,dec_values] = svmpredict(y_test(:,2),X_test(:,2),finalmodel);
MSE_predict = sum((y_test(:,2) - dec_values).^2)/numel(dec_values);
save('SVR_trained_model.mat','finalmodel') %guardamos el modelo entrenado para realizar futuras predicciones
% load('SVR_trained_model.mat','finalmodel')
%% Decision function
b = -finalmodel.rho; 

%% Plot the final result
%prediction_results = [X_test(:,2),dec_values,y_test(:,3)];
%prediction_results = sortrows(prediction_results,3); %se realiza este tipo de sort por si los proximos datos no son estrictamente crecientes
prediction_results = [X_test(:,2),dec_values];
prediction_results = sort(prediction_results);
figure
scatter(X_train(:,2),y_train(:,2),'fill','LineWidth', 0.01)
hold on
scatter(X_test(:,2),y_test(:,2),'fill','MarkerFaceColor','g','LineWidth', 0.01)
xlim([0 1]);
ylim([0 1]);
xlabel('STD Strain');
ylabel('STD Stress');
plot(prediction_results(:,1),prediction_results(:,2) + best_epsilon,':r','LineWidth', 2)
plot(prediction_results(:,1),prediction_results(:,2),'black','LineWidth', 4)
plot(prediction_results(:,1),prediction_results(:,2) - best_epsilon,':r','LineWidth', 2)
plot(TrainingSET(finalmodel.sv_indices,2),TrainingSET(finalmodel.sv_indices,1),'ro','linewidth',2);
legend('Location','NorthWest','Training Set','Test Set', 'Yi + e','Yi','Yi - e','Sv`s')
hold off