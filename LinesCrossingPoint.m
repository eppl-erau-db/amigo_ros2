function X = LinesCrossingPoint(X_1,X_2,theta_1,theta_2)

    x_1 = X_1(1,1);
    y_1 = X_1(2,1);

    x_2 = X_2(1,1);
    y_2 = X_2(2,1);


    x = (y_2 - y_1 + abs(x_2)*tand(theta_2) - abs(x_1)*tand(theta_1))/(tand(theta_1) - tand(theta_2));

    % y = (tand(theta_1) * x - abs(x_1) * tand(theta_1) + y_1);
    y = (tand(theta_1)*x + y_1 + abs(x_1)*tand(theta_1));
    X = [x; y];

    % Check if the lines are parallel
    if abs(tand(theta_1) - tand(theta_2)) < eps
        error('The lines are parallel and do not intersect.');
    end

end