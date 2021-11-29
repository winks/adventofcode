-module(day06).
-export([start/0]).

% ../input/day06/
xread() ->
    {ok, File} = file:open("input.txt",[read]),
    file:read(File, 1024 * 1024).

strlist(X, Div) ->
    case X of
        {ok, S} ->
            string:split(string:trim(S), Div, all);
        _Else ->
            []
    end.

p1x(L, Set) ->
    case L of
        []-> sets:size(Set);
        [H|T] ->
            case H of
                $\n -> p1x(T, Set);
                _ -> S2 = sets:add_element(H, Set), p1x(T, S2)
            end
    end.

p1(L, Acc) ->
    case L of 
        [] -> Acc;
        [H|T] -> p1(T, Acc + p1x(H, sets:new()))
    end.


start() ->
    L = strlist(xread(), "\n\n"),
    %erlang:display(L),
    A  = p1x("ab\nac", sets:new()),
    erlang:display(A),
    [{result, p1(L, 0)}].