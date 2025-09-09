program дкр7;
uses GraphABC, peano;
var
  startX, startY: Integer;
  scale: Integer;
  depth: Integer;

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
  f(depth, startX, startY, scale);
  Redraw;
end;

begin
  SetWindowSize(800, 600);
  ClearWindow(clWhite);
  SetPenColor(clBlack);
  OnKeyDown := KeyDown;
  startX := WindowWidth div 2 - 150;
  startY := WindowHeight div 2 + 100;
  scale := 10; 
  depth := 3; 
  LockDrawing;
  f(depth, startX, startY, scale);
  Redraw;
end.
