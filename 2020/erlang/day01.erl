-module(day01).
-export([start/0]).

% ../input/day01/
xread() ->
    {ok, File} = file:open("../input/day01/input.txt",[read]),
    Txt = file:read(File, 1024 * 1024),
    %io:fwrite("~p~n",[Txt]),
    Txt.

strlist(X) ->
    case X of
        {ok, S} ->
            string:split(S, "\n", all);
        _Else ->
            []
    end.

intlist(X) ->
    case X of
        [] -> [];
        [H|T] -> case string:to_integer(H) of
            {error, _} -> intlist(T);
            {I, _} -> [ I | intlist(T) ]
        end
    end.

find2(A,B,R) ->
    case A of
        [] -> case B of 
            [] -> 0; 
            [Hb|Tb] -> find2(Tb,Tb,Hb)
            end;
        [H|T]-> case H + R of
            2020 ->
                {result, H * R, H, R};
            _Else ->
                find2(T,B,R)
            end
    end.

find3(A,B,C,R1,R2) ->
    erlang:display({A,B,C,R1,R2}),
    
    case A of
        [] -> case B of
            [] -> case C of
                [] -> 0;
                [Hc|Tc] -> find3(C,C,Tc,R1,Hc)
                end;
            [Hb|Tb] -> find3(C,Tb,C,Hb,R2)
            end;
        [H|T]-> case H + R1 + R2 of
            2020 ->
                {result, H * R1 * R2, H, R1, R2};
            _Else ->
                find3(T,T,C,R1,R2)
            end
    end.

start() ->
    X = xread(),
    erlang:display(X),
    L1 = strlist(X),
    erlang:display(L1),
    L2 = lists:sort(intlist(L1)),
    [H|T] = L2,
    [H1|T1] = T,
    R1 = find2(T,T,H),
    R2 = find3(T1,T,L2,H1,H),
    [R1,R2].