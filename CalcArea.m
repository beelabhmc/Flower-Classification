function [Area] = CalcArea(Image)

pixels = findWhite(Image);

convFactor = (10/52.52)^2; %cm^2/pixel
areacm = pixels*convFactor; %pixels*(cm^2/pixel) = cm^2 

Area = areacm*.0001;  %convert to square meters (.01*.01) 
end