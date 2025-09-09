unit peano;
uses GraphABC;

var
  startX, startY: Integer; 
  currentX, currentY: Integer; 
  currentAngle: Real; 
  scale: Integer; 
  depth: Integer; 

procedure Right(angle: Real);
begin
  currentAngle := currentAngle - angle;
end;

procedure Left(angle: Real);
begin
  currentAngle := currentAngle + angle;
end;

procedure forwardd(dist, scale: Integer);
var
  newX, newY: Integer;
begin
  newX := currentX + Round(dist * scale * Cos(currentAngle * Pi / 180));
  newY := currentY - Round(dist * scale * Sin(currentAngle * Pi / 180));
  Line(currentX, currentY, newX, newY);
  currentX := newX;
  currentY := newY;
end;

procedure Draw(n: Real; a, scale: Integer);
begin
  if n > 0 then
  begin
    n := n - 0.5;
    Right(a);
    Draw(n, -a, scale);
    forwardd(1, scale);
    Draw(n, a, scale);
    forwardd(1, scale);
    Draw(n, -a, scale);
    Left(a);
  end;
end;

procedure F(n: Real; x, y, scale: Integer);
begin
  currentX := x;
  currentY := y;
  currentAngle := 90;
  Draw(n, 90, scale);
end;

procedure KeyDown(Key: Integer);
begin
  case Key of
    VK_Left: startX := startX - 10;
    VK_Right: startX := startX + 10;
    VK_Up: startY := startY - 10;
    VK_Down: startY := startY + 10;
    189: if scale > 1 then scale := scale - 1; 
    187: scale := scale + 1; 
    VK_W: if depth < 10 then depth := depth + 1; 
    VK_S: if depth > 1 then depth := depth - 1; 
  end;
  LockDrawing;
  ClearWindow(clWhite);
  F(depth, startX, startY, scale);
  Redraw;
end;
end.
