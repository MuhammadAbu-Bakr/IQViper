% Direction predicates
direction(up).
direction(down).
direction(left).
direction(right).

% Check if a position is safe (not occupied by snake body)
is_safe(X, Y, SnakeBody) :-
    \+ member([X, Y], SnakeBody).

% Check if a position is within bounds
in_bounds(X, Y, Width, Height) :-
    X >= 0, X < Width,
    Y >= 0, Y < Height.

% Calculate next position based on current position and direction
next_position([X, Y], up, [X, Y1]) :- Y1 is Y - 1.
next_position([X, Y], down, [X, Y1]) :- Y1 is Y + 1.
next_position([X, Y], left, [X1, Y]) :- X1 is X - 1.
next_position([X, Y], right, [X1, Y]) :- X1 is X + 1.

% Determine if a move is valid
valid_move(CurrentPos, Direction, NextPos, SnakeBody, Width, Height) :-
    next_position(CurrentPos, Direction, NextPos),
    in_bounds(X, Y, Width, Height),
    is_safe(X, Y, SnakeBody).

% Calculate Manhattan distance between two points
manhattan_distance([X1, Y1], [X2, Y2], Distance) :-
    Distance is abs(X1 - X2) + abs(Y1 - Y2).

% Find the best direction to move towards food
best_direction(CurrentPos, FoodPos, SnakeBody, Width, Height, BestDir) :-
    findall(Distance-Direction,
            (direction(Direction),
             next_position(CurrentPos, Direction, NextPos),
             valid_move(CurrentPos, Direction, NextPos, SnakeBody, Width, Height),
             manhattan_distance(NextPos, FoodPos, Distance)),
            Distances),
    sort(Distances, SortedDistances),
    SortedDistances = [_-BestDir|_]. 