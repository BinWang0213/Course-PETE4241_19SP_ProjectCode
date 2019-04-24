clear
clc
close all

%% Import the data
[~, ~, raw] = xlsread('C:\Users\bwang31\Downloads\SpatialInterpolation-20190424\SpatialInterpolation\Required_Data.xlsx','Sheet1','A2:H680401');
raw(cellfun(@(x) ~isempty(x) && isnumeric(x) && isnan(x),raw)) = {''};

%% Replace non-numeric cells with NaN
R = cellfun(@(x) ~isnumeric(x) && ~islogical(x),raw); % Find non-numeric cells
raw(R) = {NaN}; % Replace non-numeric cells

%% Create output variable
RequiredData = reshape([raw{:}],size(raw));

%% Clear temporary variables
clearvars raw R;

cmgxyz = RequiredData(:,3:5);


%% Import the MEM components for each well
[~, ~, raw] = xlsread('C:\Users\bwang31\Downloads\SpatialInterpolation-20190424\SpatialInterpolation\well_MEMcomps.xlsx','Sheet1','C2:O246');

%% Create output variable
wellMEMcomps = reshape([raw{:}],size(raw));

%% Clear temporary variables
clearvars raw filename;

addpath('dace')

D = 3;    %number of parameters to be optimized
theta = 51*ones(1,D); 
lob = 1e-9*ones(1,D);
upb = 100*ones(1,D);

[rsmodel, perf] = dacefit(wellMEMcomps(:,1:3), wellMEMcomps(:,4), @regpoly1, @correxp, theta, lob, upb);
[Sv_cmg rsmMSE] = predictor(cmgxyz, rsmodel);
SH_cmg = 0.89*Sv_cmg;
Sh_cmg = 0.84*Sv_cmg;

theta = 3.0*ones(1,D); 
lob = 1e-9*ones(1,D);
upb = 10*ones(1,D);
[rsmodel, perf] = dacefit(wellMEMcomps(:,1:3), wellMEMcomps(:,7), @regpoly1, @correxp, theta, lob, upb);
[UCS_cmg rsmMSE] = predictor(cmgxyz, rsmodel);
UCS_cmg = 1000.*UCS_cmg;

theta = 20.0*ones(1,D); 
lob = 1e-9*ones(1,D);
upb = 40*ones(1,D);
[rsmodel, perf] = dacefit(wellMEMcomps(:,1:3), wellMEMcomps(:,8), @regpoly1, @correxp, theta, lob, upb);
[E_cmg rsmMSE] = predictor(cmgxyz, rsmodel);
E_cmg = 1000.*E_cmg;

theta = 0.2*ones(1,D); 
lob = 1e-9*ones(1,D);
upb = 1.0*ones(1,D);
[rsmodel, perf] = dacefit(wellMEMcomps(:,1:3), abs(wellMEMcomps(:,9)), @regpoly1, @correxp, theta, lob, upb);
[nu_cmg rsmMSE] = predictor(cmgxyz, rsmodel);
nu_cmg = abs(nu_cmg);
%TO DO: confirm units!
InsituStress = 1000.*[Sv_cmg,SH_cmg,Sh_cmg,0.*Sh_cmg,0.*Sh_cmg,0.*Sh_cmg]';

fpath = 'C:\Users\bwang31\Downloads\SpatialInterpolation-20190424\SpatialInterpolation';
fid = fopen([fpath,'\MEMComps_cmg.txt'], 'w'); 
fprintf(fid, '**=================== GEOMECHANIC SECTION ====================\n\n');
fprintf(fid, '*GEOMECH\n');
fprintf(fid, '*GEOM3D   ** using 3D finite elements\n');
% *GPERMES  to look up table of permeability vs effective stress
fprintf(fid, '*GCOUPLING 2  ** Porosity depends on p, T, total stress\n');
fprintf(fid, '*GCFACTOR 1.0        ** geomechanic coupling factor for coupling type 2\n');

for i=1:numel(Sv_cmg)
    fprintf(fid, '*GEOROCK %d           ** rock type # %d \n',i,i);
    fprintf(fid, '   *ELASTMOD %0.10f \n',E_cmg(i));
    fprintf(fid, '   *POISSRATIO %0.10f \n',nu_cmg(i));
end
% nx  ny  nz
% 108 100 63
nx=108;ny=100;nz=63;
fprintf(fid, '\n*GEOTYPE   IJK\n');
fprintf(fid, '**         i       j       k       rocktype\n');
ii=0;
for k=1:63
    for j=1:100
        for i=1:108
            ii = ii + 1;
            fprintf(fid, '           %d       %d       %d          %d\n',i,j,k,ii);
        end
    end
end

fprintf(fid, '*STRESS3D  *ALL ** %d float \n', numel(Sv_cmg));
fprintf(fid, '%0.10f %0.10f %0.10f %0.10f %0.10f %0.10f \n', InsituStress );
fprintf(fid, '\n');
% fprintf(fid, '*PERMI *ALL ** %d float \n', numel(perm_cmg));
% fprintf(fid, '%0.10f %0.10f %0.10f %0.10f %0.10f %0.10f %0.10f %0.10f %0.10f %0.10f\n', perm_cmg);
% fprintf(fid, '\n');


% @ Overburden loads are represented by distributed load on the        
%   cap of the reservoir (*DLOADBC). 
Sv_top=1000*Sv_cmg(1:nx*ny); %MPa->kN/m2
fprintf(fid, '\n*DLOADBC3D  ** A uniform distributed load for the top of reservoir\n');
ii=0;
for j=1:100
   for i=1:108
       ii = ii + 1;
       fprintf(fid, '*IJK   %d    %d    1\n',i,j);
       fprintf(fid, '        1     2    3    4     %d ** top\n',Sv_top(ii));
   end
end

% @ Body force - gravity of the reservoir is expressed through the combination    
%   of two keywords : *GLOADBC and SPECGRAV 
fprintf(fid, '\n*SPECGRAV 2.65         ** specific gravity of a rock type\n');
fprintf(fid, '*GLOADBC              ** keyword for body force\n');
fprintf(fid, '  ** plane number       ** angle of direction (degrees)\n');
fprintf(fid, '        1:11                 0.0\n');
fclose(fid);

                         


