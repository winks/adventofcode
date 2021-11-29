-module(day05).
-export([start/0]).

xread() ->
    {ok, File} = file:open("../input/day05/input.txt",[read]),
    file:read(File, 1024 * 1024).

strlist(X) ->
    case X of
        {ok, S} ->
            string:split(string:trim(S), "\n", all);
        _Else ->
            []
    end.

bsp(L,Hi,Lo) ->
    case L of
        [$F|[]] -> Lo;
        [$L|[]] -> Lo;
        [_|[]] -> if 
            Hi - Lo > 1 -> (Hi - 1);
            true -> Hi
        end;
        [H|T] -> case H of
            $F -> bsp(T, (Hi+Lo+1) div 2, Lo);
            $L -> bsp(T, (Hi+Lo+1) div 2, Lo);
            _ -> bsp(T, Hi, (Hi+Lo+1) div 2)
        end
    end.

seats(L, Acc) ->
    case L of
        [] -> Acc;
        [H|T] -> 
            R = bsp(string:substr(H, 1, 7), 127, 0),
            X = bsp(string:substr(H, 8), 7, 0),
            A = R * 8 + X,
            seats(T, [A|Acc])
    end.

p2(L, Last) ->
    case L of
        [] -> Last;
        [H|T] -> if
            (H - Last > 1) -> Last + 1;
            true -> p2(T, H)
        end
    end.

start() ->
    L = strlist(xread()),
    S = seats(L, []),
    C1 = lists:sort(S),
    [H|T] = C1,
    C2 = p2(T, H),
    [{result, lists:last(C1)},{result, C2}].