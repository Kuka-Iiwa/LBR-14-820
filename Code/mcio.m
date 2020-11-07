clear;clc;

syms s1 s2 s3 s4 s5 s6 s7;
syms c1 c2 c3 c4 c5 c6 c7;
syms l1 l2 l3 l4;

R04 = [
    [(-s1*s3 + c1*c2*c3)*c4 + s2*s4*c1, -s1*c3 - s3*c1*c2, -(-s1*s3 + c1*c2*c3)*s4 + s2*c1*c4]
    [(s1*c2*c3 + s3*c1)*c4 + s1*s2*s4, -s1*s3*c2 + c1*c3, -(s1*c2*c3 + s3*c1)*s4 + s1*s2*c4]
    [-s2*c3*c4 + s4*c2, s2*s3, s2*s4*c3 + c2*c4]
];

syms r11 r12 r13;
syms r21 r22 r23;
syms r31 r32 r33;
R = [
    r11 r12 r13;
    r21 r22 r23;
    r31 r32 r33;
];

R47 = (R04.')*R


%[ r11*(c1*c2*c4 + c1*s2*s4) + r21*(c2*c4*s1 + s1*s2*s4) + r31*(c2*s4 - c4*s2), r12*(c1*c2*c4 + c1*s2*s4) + r22*(c2*c4*s1 + s1*s2*s4) + r32*(c2*s4 - c4*s2), r13*(c1*c2*c4 + c1*s2*s4) + r23*(c2*c4*s1 + s1*s2*s4) + r33*(c2*s4 - c4*s2)]
%[                                                             c1*r21 - r11*s1,                                                             c1*r22 - r12*s1,                                                             c1*r23 - r13*s1]
%[ r31*(c2*c4 + s2*s4) - r21*(c2*s1*s4 - c4*s1*s2) - r11*(c1*c2*s4 - c1*c4*s2), r32*(c2*c4 + s2*s4) - r22*(c2*s1*s4 - c4*s1*s2) - r12*(c1*c2*s4 - c1*c4*s2), r33*(c2*c4 + s2*s4) - r23*(c2*s1*s4 - c4*s1*s2) - r13*(c1*c2*s4 - c1*c4*s2)]