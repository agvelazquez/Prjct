clc;
clear all;
close all;

X = csvread('xxxxxx.csv',1,2);
%% standardized data
Xstd = zscore(X(1:1000,:));


%% LLE

% Based on the implementation of Saul et Rowis (03) and  Rowis et Saul (00)
% Neighbours
for k=6:10;

% Dimensions
%d = 5;
% Get dimensionality and number of dimensions
[n,D] = size(Xstd);

% Compute pairwise distances and find nearest neighbors (vectorized implementation)
[neighborhood, distance] = knnsearch(Xstd,Xstd,'k',k+1,'distance','euclidean');
neighborhood = neighborhood(:,2:end);
distance = distance(:,2:end);

% Construct reconstruction weight matrix
tol = 0;
W = zeros(n, k);
for i=1:n
    nbhd = neighborhood(i,:);
    nbhd = nbhd(nbhd ~= 0);
    z = bsxfun(@minus, Xstd(nbhd,:), Xstd(i,:)); % Shift point to origin
    C = z * z';								     % Compute local covariance
    C = C + eye(k, k) * tol * trace(C);		     % Regularization of covariance (if K > D)
    wi = C \ ones(k, 1);                         % Solve linear system
    wi = wi / sum(wi);                           % Make sure that sum is 1
end

% sparse cost matrix M = (I-W)'*(I-W).
M = sparse(1:n, 1:n, ones(1, n), n, n, 4 * k * n);
for i=1:n
    w = W(:,i);
    j = neighborhood(:,i);
    indices = find(j ~= 0 & ~isnan(w));
    j = j(indices);
    w = w(indices);
    M(i, j) = M(i, j) - w';
    M(j, i) = M(j, i) - w;
    M(j, j) = M(j, j) + w * w';
end
    
% The embedding is computed from the bottom eigenvectors of this cost matrix
error = zeros(D,k);
W = W';
for no_dims=1:D; %l = numero de dimensiones
    options.disp   = 0;
    options.isreal = 1;
    options.issym  = 1;
    [mappedX, eigenvals] = eigs(M, no_dims + 1, tol, options);          % only need bottom (no_dims + 1) eigenvectors
    [eigenvals, ind] = sort(diag(eigenvals), 'ascend');
    %throw away zero eigenvector/value
    eigenvals = eigenvals(2:no_dims + 1);
    mappedX = mappedX(:,ind(2:no_dims + 1));
    % obtengo los k vecinos mas cercanos del mapeo
    [IDX,Dist] = knnsearch(mappedX,mappedX,'k',k+1,'distance','euclidean');
    IDX = IDX(:,2:end);
    Dist = Dist(:,2:end);
    % con la matriz W reconstruyo cada punto del mapeo
    %
    Yhat = zeros(size(mappedX));
    Yneighbours = zeros(k,no_dims);
        for j=1:n; %samples
            for i=1:(k) %vecinos
                Yneighbours(i,:) = (W(j,i) * mappedX(IDX(j,i),:));    
            end
            Yhat(j,:) = nansum(Yneighbours);
        end
% error> la diferencia entre la reconstruccion y el punto original
    error(no_dims,k) = norm(mappedX-Yhat);
end
end    
dimensiones = [1:1:12];
figure
plot(error(:,2),dimensiones,error(:,4),dimensiones,error(:,6),dimensiones,error(:,8),dimensiones,error(:,10),dimensiones)
title('Dimensions & Reconstruction error')
legend('k=10')
xlabel('Number of dimensions')
ylabel('Error')