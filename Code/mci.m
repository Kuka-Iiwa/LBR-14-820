clear; clc;

%Dimensões do Robo
a1=1; a2=1; a3=1; % Links do 3R cotovelar
a7=1; % Comprimento do centro do pinho esferico ao efetuador


% POSE desejada
POSE1 = [ 
 1  0  0    2;
 0  1  0    0;
 0  0  1    2;
 0  0  0    1;
]; % Posição home, entretanto com theta2 = 90° e theta6 = -90°

POSE2 = [ 
 1  0  0    2;
 0  0 -1   -1;
 0  1  0    1;
 0  0  0    1;
]; % Posição home, entretanto com theta2 = theta3 = 90° e theta6 = -90°


POSE3 = [                       %theta1 = -90;
    0    1  0   0;              %theta2 =  60;
   -1    0  0   -1.732051;      %theta3 =   0;
    0    0  1   2;              %theta4 =  60;
    0    0  1   1;              %theta5 =   0;
];                              %theta6 =-120;
                                %theta7 =   0;

POSE = POSE3;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Primeiro achar o centro do punho
Xc = POSE(1,4) - a7*POSE(1,3);
Yc = POSE(2,4) - a7*POSE(2,3);
Zc = POSE(3,4) - a7*POSE(3,3);
%Exibir ponto C 
[Xc;Yc;Zc]

% INDICE - MCI de posição
% 1 - Braço frente  Cotovelo Cima
% 2 - Braço frente  Cotovelo Baixo
% 3 - Braço frente  Cotovelo Esquerda
% 4 - Braço frente  Cotovelo Direita
% 5 - Braço trás    Cotovelo Cima
% 6 - Braço trás    Cotovelo Baixo
% 7 - Braço trás    Cotovelo Esquerda
% 8 - Braço trás    Cotovelo Direita

%Lei dos Cossenos
r2        = Xc^2 + Yc^2 + (Zc-a1)^2;       % R^2
rl        = sqrt(Xc^2 + Yc^2);
D         = (a3^2 + a2^2 - r2  ) / (2*a2*a3);
E         = (r2   + a2^2 - a3^2) / (2*sqrt(r2)*a3);

% Theta 1
theta1(1) = atan2(Yc,Xc);
theta1(2) = theta1(1);
theta1(3) = theta1(1) + atan2(-sqrt(1-E^2),E);
theta1(4) = theta1(1) + atan2( sqrt(1-E^2),E);
theta1(5) = theta1(1) + pi;
theta1(6) = theta1(2) + pi;
theta1(7) = theta1(4) + pi;
theta1(8) = theta1(3) + pi;

% Theta 4
theta4(1) = pi - atan2( sqrt(1-D^2),D);
theta4(2) = pi - atan2(-sqrt(1-D^2),D);
theta4(3) = theta4(1);
theta4(4) = theta4(2);
theta4(5) = -theta4(2);
theta4(6) = -theta4(1);
theta4(7) = -theta4(2);
theta4(8) = -theta4(1);

% Theta 3
theta3(1) =  0;
theta3(2) =  0;
theta3(3) = pi/2;
theta3(4) = pi/2;
theta3(5) = theta3(1);
theta3(6) = theta3(2);
theta3(7) = theta3(3);
theta3(8) = theta3(4);

% Theta 2
theta2(1) = pi/2 - atan2(Zc-a1,rl) + atan2(-sqrt(1-E^2),E);
theta2(2) = pi/2 - atan2(Zc-a1,rl) + atan2( sqrt(1-E^2),E);
theta2(3) = pi/2 - atan2(Zc-a1,rl);
theta2(4) = pi/2 - atan2(Zc-a1,rl);
theta2(5) = pi+theta2(1);
theta2(6) = pi+theta2(2);
theta2(7) = pi+theta2(3);
theta2(8) = pi+theta2(4);



% INDICE - MCI de Orientação - Punho esferico
% A - Punho Normal
% B - Punho Invertido

% Calculo dos Theta
for i = 1:8
    theta5(i) = atan2( -cos(theta1(i))*sin(theta2(i)-theta4(i))*POSE(1,3) - sin(theta1(i))*sin(theta2(i)-theta4(i))*POSE(2,3) + cos(theta2(i)-theta4(i))*POSE(3,3) ,                         cos(theta1(i))*cos(theta2(i)-theta4(i))*POSE(1,3) + sin(theta1(i))*cos(theta2(i)-theta4(i))*POSE(2,3) + sin(theta2(i)-theta4(i))*POSE(3,3) );

    theta5b(i)= theta5(i)+pi;

    theta6(i) = atan2( sqrt(1-(sin(theta1(i))*POSE(1,3) - cos(theta1(i))*POSE(2,3))^2),                         sin(theta1(i))*POSE(1,3) - cos(theta1(i))*POSE(2,3) );

    theta6b(i)= atan2(-sqrt(1-(sin(theta1(i))*POSE(1,3) - cos(theta1(i))*POSE(2,3))^2),                         sin(theta1(i))*POSE(1,3) - cos(theta1(i))*POSE(2,3) );

    theta7(i) = atan2(             sin(theta1(i))*POSE(1,2) - cos(theta1(i))*POSE(2,2),                        -sin(theta1(i))*POSE(1,1) + cos(theta1(i))*POSE(2,1));

    theta7b(i)= theta7(i)+pi;
end

% INDICE - MCI COMPLETO
% 1  - Braço frente  Cotovelo Cima      Punho Normal
% 2  - Braço frente  Cotovelo Baixo     Punho Normal
% 3  - Braço frente  Cotovelo Esquerda  Punho Normal
% 4  - Braço frente  Cotovelo Direita   Punho Normal
% 5  - Braço trás    Cotovelo Cima      Punho Normal
% 6  - Braço trás    Cotovelo Baixo     Punho Normal
% 7  - Braço trás    Cotovelo Esquerda  Punho Normal
% 8  - Braço trás    Cotovelo Direita   Punho Normal
% 9  - Braço frente  Cotovelo Cima      Punho Invertido
% 10 - Braço frente  Cotovelo Baixo     Punho Invertido
% 11 - Braço frente  Cotovelo Esquerda  Punho Invertido
% 12 - Braço frente  Cotovelo Direita   Punho Invertido
% 13 - Braço trás    Cotovelo Cima      Punho Invertido
% 14 - Braço trás    Cotovelo Baixo     Punho Invertido
% 15 - Braço trás    Cotovelo Esquerda  Punho Invertido
% 16 - Braço trás    Cotovelo Direita   Punho Invertido

for i = 1:8
    sol (i  ,:) = [theta1(i) theta2(i) theta3(i) theta4(i)  theta5(i)  theta6(i)  theta7(i)]*180/pi;
    sol (i+8,:) = [theta1(i) theta2(i) theta3(i) theta4(i) theta5b(i) theta6b(i) theta7b(i)]*180/pi;
end

%Solução completa
%sol

%Solução apenas de MCI
sol(1:8,1:4)
