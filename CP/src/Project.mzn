include "globals.mzn";

int: WIDTH;
int: HEIGHT;
int: n;

array[1..n, 1..2] of int: presents_dimensions;
array[1..n] of var 0..WIDTH: corners_x;
array[1..n] of var 0..HEIGHT: corners_y;
array[1..n] of 0..WIDTH: durations_x;
array[1..n] of 0..HEIGHT: durations_y;

constraint cumulative(corners_x, presents_dimensions[.., 1], presents_dimensions[.., 2], HEIGHT);
constraint cumulative(corners_y, presents_dimensions[.., 2], presents_dimensions[.., 1], WIDTH);
constraint forall(i in 1..n) (corners_x[i] + presents_dimensions[i, 1] <= WIDTH);
constraint forall(i in 1..n) (corners_y[i] + presents_dimensions[i, 2] <= HEIGHT);

% PLACING A PRESENT TO THE LEFT/RIGHT/ABOVE/BELOW OF AN OTHER TO AVOID OVERLAPPING
%constraint forall(i in 1..n, j in i+1..n) (corners_x[i] + presents_dimensions[i, 1] <= corners[j, 1] \/
                                            %corners_x[j] + presents_dimensions[j, 1] <= corners[i, 1] \/
                                            %corners[i, 2] + presents_dimensions[i, 2] <= corners[j, 2] \/
                                           % corners[j, 2] + presents_dimensions[j, 2] <= corners[i, 2]);


% avoiding overlap using global constraint "diffn"
constraint diffn(corners_x, corners_y, presents_dimensions[.., 1], presents_dimensions[.., 2]);

% breaking symmetry
constraint corners_x[n] < WIDTH div 2 /\ corners_y[n] < HEIGHT div 2;

ann: search_ann;
search_ann = int_search(corners_x ++ corners_y, dom_w_deg, indomain_min);

solve :: search_ann satisfy;