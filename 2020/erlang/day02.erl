-module(day02).
-export([start/0]).

xread() ->
    {ok, File} = file:open("../input/day02/input.txt",[read]),
    file:read(File, 1024 * 1024).

strlist(X) ->
    case X of
        {ok, S} ->
            string:split(S, "\n", all);
        _Else ->
            []
    end.

check1(S) ->
    P1 = string:split(S, ":", all),
    Pass = string:trim(lists:nth(2, P1)),
    P2 = string:split(P1, " ", all),
    Char = hd(lists:nth(2, P2)),
    P3 = string:split(lists:nth(1, P2), "-", all),
    Min = lists:nth(1, P3),
    Max = lists:nth(2, P3),
    Len = length(lists:filter(fun(X) -> X == Char end, Pass)),
    Min1 = string:to_integer(Min),
    Max1 = string:to_integer(Max),
    case Min1 of
        {error, _} -> false;
        {IMin, _} -> 
            case Max1 of
                {error, _} -> false;
                {IMax, _} -> 
                    if Len < IMin ->
                        false;
                    Len > IMax ->
                        false;
                    true ->
                        true
                    end
            end
    end.


check2(S) ->
    P1 = string:split(S, ":", all),
    Pass = string:trim(lists:nth(2, P1)),
    P2 = string:split(P1, " ", all),
    Char = hd(lists:nth(2, P2)),
    P3 = string:split(lists:nth(1, P2), "-", all),
    {One, _} = string:to_integer(lists:nth(1, P3)),
    {Two, _} = string:to_integer(lists:nth(2, P3)),
    C1 = lists:nth(One, Pass),
    C2 = lists:nth(Two, Pass),
    ((C1 == Char) xor (C2 == Char)).
        

start() ->
    L = strlist(xread()),
    C1 = lists:filter(fun(X) -> case length(X) of 0 -> false; _ -> check1(X) end end, L),
    C2 = lists:filter(fun(X) -> case length(X) of 0 -> false; _ -> check2(X) end end, L),
    [{result, length(C1)},{result, length(C2)}].