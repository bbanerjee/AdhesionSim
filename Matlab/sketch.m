function sketch

  rStem = 0.5;   % Stem radius
  lStem = 1.0;   % Stem length
  lPlate = 2.5;  % Distance between stems (plate length)
  tPlate = 1.0;  % Plate thickness
  tCup = 0.296;  % Cup thickness
  rCupOut = 1.5; % Cup outer radius
  rCupIn = 1.35; % Cup inner radius
  %
  % Derived parameters
  %
  theta = asin(rStem/rCupOut);
  xc = 0.0;
  yc = -(rCupOut*cos(theta) - tCup);
  x1 = 0.0;
  y1 = 0.0;
  x2 = 0.0;
  y2 = tCup;
  x3 = 0.0;
  y3 = y2+lStem;
  x4 = 0.0;
  y4 = y3+tPlate;
  x5 = -0.5*lPlate;
  y5 = y4;
  x6 = x5;
  y6 = y3;
  x7 = -rStem;
  y7 = y6;
  x8 = x7;
  y8 = y2;
  x9 = -sqrt(rCupOut^2-yc^2);
  y9 = 0.0;
  x10 = -sqrt(rCupIn^2-yc^2);
  y10 = 0.0;
  x11 = 0.0;
  y11 = rCupIn + yc;

  plot([xc x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11], ...
       [yc y1 y2 y3 y4 y5 y6 y7 y8 y9 y10 y11], 'k-');
  axis equal;
  

