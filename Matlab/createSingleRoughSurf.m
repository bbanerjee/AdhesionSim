%
% Create an Abaqus input file for one rough surface
%
function createSingleRoughSurf(n, refineLevel, domainLen)

  %
  % Define size of the grid
  %
  %n = 0;
  %n = 4;
  gridsize = 2^(2+n);
  %refineLevel = 4;

  %
  % Create the mesh 
  %
  bot = -1;
  startNode = 0;
  startElem = 0;
  gridspacing = 1.2;
  %domainLen = 7;  % The size of the block is 7 mm x 7 mm
  [nodeBot, elemBot] = createMesh(n, gridsize, gridspacing, bot, startNode, startElem, ...
                                  refineLevel, domainLen);
  plotMesh(nodeBot, elemBot);
  

  %
  % Select boundary condition nodes for bottom part
  %
  [nodeFixedBot, nodeXsymmBot, nodeYsymmBot] = selectNodes(nodeBot, bot);

  %
  % Select contact elements for the bottom part (master)
  %
  [contactElemBot] = selectElems(elemBot, bot);

  %
  % Select contact nodes for the bottom part
  %
  [contactNodeBot] = selectContactNodes(nodeBot);

  %
  % Write data in Abaqus format
  %
  fid = fopen('AdhesionSingleSurf.inp','w');
  writeAbaqusHeader(fid);
  writeAbaqusMesh(fid, nodeBot, elemBot, nodeBot, elemBot);
  fprintf(fid, '** ASSEMBLY\n');
  fprintf(fid, '*Assembly, name=Assembly\n');
  fprintf(fid, '*Instance, name=BottomBlock-1, part=BottomBlock\n');
  fprintf(fid, '*End Instance\n');
  fprintf(fid, '**\n');
  fprintf(fid, '*Nset, nset=nodeFixedBot, internal, instance=BottomBlock-1\n');
  writeAbaqusNodeSet(fid, nodeFixedBot);
  fprintf(fid, '*Nset, nset=nodeXsymmBot, internal, instance=BottomBlock-1\n');
  writeAbaqusNodeSet(fid, nodeXsymmBot);
  fprintf(fid, '*Nset, nset=nodeYsymmBot, internal, instance=BottomBlock-1\n');
  writeAbaqusNodeSet(fid, nodeYsymmBot);
  fprintf(fid, '*Nset, nset=contactNodeBot, internal, instance=BottomBlock-1\n');
  writeAbaqusNodeSet(fid, contactNodeBot);
  writeAbaqusNodeSurface(fid, contactNodeBot, 'contactNodeBot', bot);
  writeAbaqusElemSurface(fid, contactElemBot, 'BottomBlock-1', bot);
  fprintf(fid, '*End Assembly\n');
  writeAbaqusMat(fid);
  writeAbaqusInteraction(fid);
  writeAbaqusStep(fid);
  fclose(fid);

%
% Plot the mesh
%
function plotMesh(node, elem)
  numNode = size(node(:,1)); 
  numElem = size(elem(:,1)); 

  for ii=1:numElem
    el = elem(ii,:);
    n1 = el(2);
    n2 = el(3);
    n3 = el(4);
    n4 = el(5);
    botx = [node(n1,2) node(n2,2), node(n3,2) node(n4,2) node(n1,2)];
    boty = [node(n1,3) node(n2,3), node(n3,3) node(n4,3) node(n1,3)];
    botz = [node(n1,4) node(n2,4), node(n3,4) node(n4,4) node(n1,4)];
    plot3(botx, boty, botz, 'b-'); hold on;
    n1 = el(6);
    n2 = el(7);
    n3 = el(8);
    n4 = el(9);
    botx = [node(n1,2) node(n2,2), node(n3,2) node(n4,2) node(n1,2)];
    boty = [node(n1,3) node(n2,3), node(n3,3) node(n4,3) node(n1,3)];
    botz = [node(n1,4) node(n2,4), node(n3,4) node(n4,4) node(n1,4)];
    plot3(botx, boty, botz, 'm-'); hold on;
  end
   
%
% Write an Abaqus format file
%
function writeAbaqusHeader(fid)

  %
  % Header
  %
  fprintf(fid, '*Heading\n');
  fprintf(fid, '** Job name: Job-4 Model name: Adhesion-1\n');
  fprintf(fid, '*Preprint, echo=NO, model=NO, history=NO, contact=NO\n');
  fprintf(fid, '** PARTS\n');

function writeAbaqusMesh(fid, nodeBot, elemBot, nodeTop, elemTop)

  %
  % Bottom part first
  %
  fprintf(fid, '*Part, name=BottomBlock\n');
  fprintf(fid, '*Node\n');
  numNodeBot = size(nodeBot(:,1));
  for ii=1:numNodeBot
    fprintf(fid, '%5d, %16.5f, %16.5f, %16.5f\n', ...
      ii, nodeBot(ii,2), nodeBot(ii,3), nodeBot(ii,4));
  end
  fprintf(fid, '*Element, type=C3D8RH\n');
  numElemBot = size(elemBot(:,1));
  for ii=1:numElemBot
    fprintf(fid, '%5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d\n', ...
      ii, elemBot(ii,2), elemBot(ii,3), elemBot(ii,4), elemBot(ii,5), ...
      elemBot(ii,6), elemBot(ii,7), elemBot(ii,8), elemBot(ii,9));
  end
  fprintf(fid, '*Nset, nset=BotMesh, internal, generate\n');
  fprintf(fid, '    1, %5d,    1\n', numNodeBot);
  fprintf(fid, '*Elset, elset=BotMesh, internal, generate\n');
  fprintf(fid, '    1, %5d,    1\n', numElemBot);
  fprintf(fid, '** Section: BottomSection\n');
  fprintf(fid, '*Solid Section, elset=BotMesh, material="Soft Surface"\n');
  fprintf(fid, ',\n');
  fprintf(fid, '*End Part\n');

function writeAbaqusNodeSet(fid, nodeSet)

  numNode = length(nodeSet);
  for ii=1:numNode
    if ((mod(ii,16) == 0) | (ii==numNode))
      fprintf(fid, ' %5d\n', nodeSet(ii));
    else
      fprintf(fid, ' %5d,', nodeSet(ii));
    end
  end

function writeAbaqusNodeSurface(fid, nodeSet, setName, loc)

  fprintf(fid, '*Surface, type=NODE, name=%s, internal\n', setName);
  fprintf(fid, '%s, 1.0\n', setName);

function writeAbaqusElemSurface(fid, elemSet, name, loc)

  numElem = length(elemSet);
  if (loc == -1)
    fprintf(fid, '*Elset, elset=BottomContactSurf, internal, instance=%s\n', name); 
    for ii=1:numElem
      if ((mod(ii,16) == 0) | (ii == numElem))
        fprintf(fid, ' %5d\n', elemSet(ii));
      else
        fprintf(fid, ' %5d,', elemSet(ii));
      end
    end
    fprintf(fid, '*Surface, type=ELEMENT, name=BottomContactSurf\n');
    fprintf(fid, 'BottomContactSurf, S2\n');
  else
    fprintf(fid, '*Elset, elset=TopContactSurf, internal, instance=%s\n', name); 
    for ii=1:numElem
      if ((mod(ii,16) == 0) | (ii == numElem))
        fprintf(fid, ' %5d\n', elemSet(ii));
      else
        fprintf(fid, ' %5d,', elemSet(ii));
      end
    end
    fprintf(fid, '*Surface, type=ELEMENT, name=TopContactSurf\n');
    fprintf(fid, 'TopContactSurf, S1\n');
  end

function writeAbaqusInteraction(fid)

  fprintf(fid, '**INTERACTION PROPERTIES\n');
  fprintf(fid, '*Surface Interaction, name=Contact-1\n');
  fprintf(fid, '1.,\n');
  fprintf(fid, '*Surface Behavior, pressure-overclosure=HARD\n');
  fprintf(fid, '**INTERACTIONS\n');
  fprintf(fid, '*Contact Pair, interaction=Contact-1, type=SURFACE TO SURFACE\n');
  fprintf(fid, 'BottomContactSurf, BottomContactSurf\n');

function writeAbaqusStep(fid)

  fprintf(fid, '** STEP: Step-1\n');
  fprintf(fid, '*Step, name=Step-1, nlgeom=YES\n');
  fprintf(fid, 'push contact\n');
  fprintf(fid, '*Static\n');
  fprintf(fid, '1., 1., 1e-05, 1.\n');
  fprintf(fid, '** BOUNDARY CONDITIONS\n');
  fprintf(fid, '** Name: BC-1 Type: Displacement/Rotation\n');
  fprintf(fid, '*Boundary\n');
  fprintf(fid, 'NodeFixedBot, 3, 3, 0.0\n');
  fprintf(fid, 'NodeXSymmBot, 1, 1, 0.0\n');
  fprintf(fid, 'NodeYSymmBot, 2, 2, 0.0\n');
  fprintf(fid, '** OUTPUT REQUESTS\n');
  fprintf(fid, '*Restart, write, frequency=0\n');
  fprintf(fid, '*Output, field, variable=PRESELECT\n');
  fprintf(fid, '*Output, history, variable=PRESELECT\n');
  fprintf(fid, '*End Step\n');

function writeAbaqusMat(fid)
  %
  % Create materials
  %
  fprintf(fid, '** MATERIALS\n');
  fprintf(fid, '*Material, name="Soft Surface"\n');
  fprintf(fid, '*Density\n');
  fprintf(fid, ' 1.00\n');
  fprintf(fid, '*Elastic\n');
  fprintf(fid, ' 1.00, 0.49\n');
  fprintf(fid, '*Material, name="Elastomer"\n');
  fprintf(fid, '*Density\n');
  fprintf(fid, ' 1.00\n');
  fprintf(fid, '*Elastic\n');
  fprintf(fid, ' 0.10, 0.49\n');

%
% Select contact nodes (for surface to node contact)
%
function [contactNode] = selectContactNodes(node)

  numNode = size(node(:,1));
  contactNode = node(1:numNode/3,1)';

%
% Select contact elements
%
function [contactElem] = selectElems(elem, loc)

  %
  % Locate the elements connected to the rough surface
  %
  numElem = size(elem(:,1));
  if (loc == -1)
     count = 0;
     for ii=numElem/2+1:numElem
        count = count+1;
        contactElem(count) = elem(ii,1); 
     end
  else
     count = 0;
     for ii=1:numElem/2
        count = count+1;
        contactElem(count) = elem(ii,1); 
     end
  end

%
% Select boundary condition nodes 
%
function [nodeFixed, nodeXsymm, nodeYsymm] = selectNodes(node, loc)

  %
  % Locate the fixed nodes
  %
  numNode = size(node(:,1));
  if (loc == -1)
    
    % Sort nodes in ascending order of z
    nodeSort = sortrows(node, 4);
    zmin = nodeSort(1,4);
    count = 0;
    for ii=1:numNode
      znode = nodeSort(ii,4);
      if (znode > zmin)
        break;
      end
      count = count+1;
      nodeFixed(count) = nodeSort(ii,1);
    end
  else

    % Sort nodes in descending order of z
    nodeSort = sortrows(node, -4);
    zmax = nodeSort(1,4);
    count = 0;
    for ii=1:numNode
      znode = nodeSort(ii,4);
      if (znode < zmax)
        break;
      end
      count = count+1;
      nodeFixed(count) = nodeSort(ii,1);
    end
  end
  %nodeSort
  %nodeFixed

  %
  % Locate the nodes at x = 0 
  %
  nodeSort = sortrows(node, 2);
  xmin = 0.0;
  count = 0;
  for ii=1:numNode
    xnode = nodeSort(ii,2);
    if (xnode > xmin)
      break;
    end
    count = count+1;
    nodeXsymm(count) = nodeSort(ii,1);
  end
  %nodeSort
  %nodeXsymm

  %
  % Locate the nodes at y = 0 
  %
  nodeSort = sortrows(node, 3);
  ymin = 0.0;
  count = 0;
  for ii=1:numNode
    ynode = nodeSort(ii,3);
    if (ynode > ymin)
      break;
    end
    count = count+1;
    nodeYsymm(count) = nodeSort(ii,1);
  end
  %nodeSort
  %nodeYsymm
  
  %
  % Sort everything
  %
  nodeFixed = sort(nodeFixed);
  nodeXsymm = sort(nodeXsymm);
  nodeYsymm = sort(nodeYsymm);
  %nodeFixed
  %nodeXsymm
  %nodeYsymm

%
% Create a mesh for block with a rough surface
%
function [node, elem] = createMesh(n, gridsize, gridspacing, loc, startNode, startElem, ...
                                   refineLevel, domainLen)

  %
  % Create the surface
  %
  [x, y, z, gridsize, gridspacing] = createSurf(n, gridsize, gridspacing, refineLevel, domainLen);

  %
  % Push surface below/above datum depending on loc
  %
  zmin = min(min(z));
  zmax = max(max(z));
  if (loc == -1)
    for ii=1:gridsize
      for jj=1:gridsize
        t = (z(ii,jj)-zmin)/(zmax-zmin);
        znew(ii,jj) = (t-1)*gridspacing*3;
      end
    end
  else
    for ii=1:gridsize
      for jj=1:gridsize
        t = (z(ii,jj)-zmin)/(zmax-zmin);
        znew(ii,jj) = t*gridspacing*3;
      end
    end
  end

  %
  % Create z values for first and second layer
  %
  if (loc == -1)
    zmin = min(min(znew));
    zlayer1  = zmin - gridspacing;
    zlayer2  = zmin - 2*gridspacing;
  else
    zmax = max(max(znew));
    zlayer1  = zmax + gridspacing;
    zlayer2  = zmax + 2*gridspacing;
  end

  %
  % Create the nodes for the surface
  %
  numNode = startNode;
  for jj=1:gridsize
    for ii=1:gridsize
      numNode = numNode + 1;
      nodeid(numNode) = numNode;
      nodex(numNode) = x(ii,jj);
      nodey(numNode) = y(ii,jj);
      nodez(numNode) = znew(ii,jj);
    end
  end
  %
  % Create the nodes for the first layer
  %
  numNodeLayer1 = numNode;
  for ii=1:numNodeLayer1
    numNode = numNode+1;
    nodeid(numNode) = numNode;
    nodex(numNode) = nodex(ii);
    nodey(numNode) = nodey(ii);
    nodez(numNode) = 0.5*(zlayer2+nodez(ii));
  end
  %
  % Create the nodes for the second layer
  %
  for ii=1:numNodeLayer1
    numNode = numNode+1;
    nodeid(numNode) = numNode;
    nodex(numNode) = nodex(ii);
    nodey(numNode) = nodey(ii);
    nodez(numNode) = zlayer2;
  end
  %
  % Put in one variable
  %
  node = [nodeid' nodex' nodey' nodez'];

  %
  % Create the elements (bottom up)
  %
  numElem = startElem;
  if (loc == 1)
    %
    % First layer
    %
    for ii=1:gridsize-1
      for jj=1:gridsize-1
        nodeID = startNode + (jj-1)*gridsize + ii;
        numElem = numElem + 1;
        node1 = nodeID;
        node2 = node1+1;
        node3 = node2+gridsize;
        node4 = node3-1;
        node5 = node1 + numNodeLayer1;
        node6 = node2 + numNodeLayer1;
        node7 = node3 + numNodeLayer1;
        node8 = node4 + numNodeLayer1;
        elem(numElem,:) = [numElem node1 node2 node3 node4 node5 node6 node7 node8];
      end
    end
    %
    % Second layer
    %
    for ii=1:gridsize-1
      for jj=1:gridsize-1
        nodeID = startNode + numNodeLayer1 + (jj-1)*gridsize + ii;
        numElem = numElem + 1;
        node1 = nodeID;
        node2 = node1+1;
        node3 = node2+gridsize;
        node4 = node3-1;
        node5 = node1 + numNodeLayer1;
        node6 = node2 + numNodeLayer1;
        node7 = node3 + numNodeLayer1;
        node8 = node4 + numNodeLayer1;
        elem(numElem,:) = [numElem node1 node2 node3 node4 node5 node6 node7 node8];
      end
    end
  else
    %
    % First layer
    %
    for ii=1:gridsize-1
      for jj=1:gridsize-1
        nodeID = startNode + 2*numNodeLayer1 + (jj-1)*gridsize + ii;
        numElem = numElem + 1;
        node1 = nodeID;
        node2 = node1+1;
        node3 = node2+gridsize;
        node4 = node3-1;
        node5 = node1 - numNodeLayer1;
        node6 = node2 - numNodeLayer1;
        node7 = node3 - numNodeLayer1;
        node8 = node4 - numNodeLayer1;
        elem(numElem,:) = [numElem node1 node2 node3 node4 node5 node6 node7 node8];
      end
    end
    %
    % Second layer
    %
    for ii=1:gridsize-1
      for jj=1:gridsize-1
        nodeID = nodeID+1;
        nodeID = startNode + numNodeLayer1 + (jj-1)*gridsize + ii;
        numElem = numElem + 1;
        node1 = nodeID;
        node2 = node1+1;
        node3 = node2+gridsize;
        node4 = node3-1;
        node5 = node1 - numNodeLayer1;
        node6 = node2 - numNodeLayer1;
        node7 = node3 - numNodeLayer1;
        node8 = node4 - numNodeLayer1;
        elem(numElem,:) = [numElem node1 node2 node3 node4 node5 node6 node7 node8];
      end
    end
  end

%
%  Create surface 
%
function [x, y, surfelev, gridsize, gridspacing] = createSurf(n, gridsize, gridspacing, refineLevel, domainLen)

  %
  % Create the surface elevations
  %
  surfelev = plasma(n);

  if (refineLevel > 1)
    %
    % Update gridsize
    %
    gridsizeupd = refineLevel*(gridsize-1) + 1;

    %
    % Fill in the updated grid with known values
    %
    for ii=1:gridsize
      row = refineLevel*(ii-1) + 1;
      for jj=1:gridsize
        col = refineLevel*(jj-1) + 1;
        elevnew(row,col) = surfelev(ii,jj);
      end
    end
    %surfelev
    %elevnew

    %
    % Interpolate the unknown values
    %
    for row=1:gridsizeupd
      rowfloor = floor((row-1)/refineLevel)+1;
      if (rowfloor > gridsize)
        endii = rowfloor-1;
        startii = endii-1;
      elseif (rowfloor == gridsize)
        endii = rowfloor;
        startii = endii-1;
      else
        startii = rowfloor;
        endii = startii+1;
      end
      startrow = refineLevel*(startii-1) + 1;
      endrow = refineLevel*(endii-1) + 1;
      xi = (2*row-startrow-endrow)/(endrow-startrow);
      %rows = [row startii endii startrow endrow xi]
      for col=1:gridsizeupd
        colfloor = floor((col-1)/refineLevel)+1;
        if (colfloor > gridsize)
          endjj = colfloor-1;
          startjj = endjj-1;
        elseif (colfloor == gridsize)
          endjj = colfloor;
          startjj = endjj-1;
        else
          startjj = colfloor;
          endjj = startjj+1;
        end
        startcol = refineLevel*(startjj-1) + 1;
        endcol = refineLevel*(endjj-1) + 1;
        eta = (2*col-startcol-endcol)/(endcol-startcol);
        %cols = [col startjj endjj startcol endcol eta]
        z1 = elevnew(startrow,startcol);
        z2 = elevnew(startrow,endcol);
        z3 = elevnew(endrow,endcol);
        z4 = elevnew(endrow,startcol);
        N1 = 1/4*(1-xi)*(1-eta);
        N2 = 1/4*(1-xi)*(1+eta);
        N3 = 1/4*(1+xi)*(1+eta);
        N4 = 1/4*(1+xi)*(1-eta);
        elevnew(row,col) = N1*z1 + N2*z2 + N3*z3 + N4*z4;
      end
    end
    gridsize = gridsizeupd;
    surfelev = elevnew;
  end

  %
  % Create the (x,y) locations for the surface
  %
  for ii=1:gridsize
    xloc = (ii-1)*gridspacing;
    for jj=1:gridsize
      yloc = (jj-1)*gridspacing;
      x(ii,jj) = xloc;
      y(ii,jj) = yloc;
    end
  end

  %
  % Scale the coordinates based on the size of the domain
  %
  xmax = max(max(x));
  zmin = min(min(surfelev));
  zmax = max(max(surfelev));
  scalefac = domainLen/xmax;
  zscalefac = 0.1*domainLen/(zmax-zmin);
  for ii=1:gridsize
    for jj=1:gridsize
      x(ii,jj) = x(ii,jj)*scalefac;
      y(ii,jj) = y(ii,jj)*scalefac;
      surfelev(ii,jj) = surfelev(ii,jj)*zscalefac;
    end
  end
  gridspacing = gridspacing*scalefac;

% Elegant, fast, non-recursive way to create a plasma 
% fractal PLASMA(n) takes one argument n , where 
% 2^(2+n) is the size of the square plasma matrix. 
% The default value of n is 6, which gives a
% 256 x 256 matrix
%
% Arjun Viswanathan 1999
function a=plasma(n)

  randn('state',sum(clock*100));
  t=cputime;
  a=rand(4);
  if nargin<1
     n=6;
  end

  for i=1:n;
     r=size(a,1);c=size(a,2);
     xi=[1:(r-1)/(2*r-1):r];
     yi=[1:(c-1)/(2*c-1):c];
     a=interp2(a,xi,yi','cubic');
     step=2^(-i);
     dev=rand(size(a)).*step-2*step;
     a=a+dev;
  end
