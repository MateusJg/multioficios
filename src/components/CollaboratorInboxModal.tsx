import React, { useState, useEffect } from 'react';
import { 
  X, 
  MessageSquare, 
  User, 
  Clock, 
  ShieldCheck, 
  ChevronRight, 
  HardHat, 
  Smartphone,
  Radio
} from 'lucide-react';
import { Collaborator, ActiveUserProfile } from '../types';
import { subscribeToCollaboratorChats, ChatSummary } from '../services/firebase';

interface CollaboratorInboxModalProps {
  activeProfile: ActiveUserProfile;
  collaborator: Collaborator;
  onOpenChat: (collaborator: Collaborator, directChatId?: string) => void;
  onClose: () => void;
}

export const CollaboratorInboxModal: React.FC<CollaboratorInboxModalProps> = ({
  activeProfile,
  collaborator,
  onOpenChat,
  onClose,
}) => {
  const [chats, setChats] = useState<ChatSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = subscribeToCollaboratorChats(collaborator.id, (remoteChats) => {
      setChats(remoteChats);
      setLoading(false);
    });

    return () => {
      unsubscribe();
    };
  }, [collaborator.id]);

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-stone-900/60 backdrop-blur-xs flex items-center justify-center p-3 sm:p-6 animate-in fade-in duration-200">
      <div 
        className="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl border border-stone-200 overflow-hidden flex flex-col max-h-[85vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 sm:p-5 bg-stone-900 text-white flex items-center justify-between border-b border-stone-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-amber-600 flex items-center justify-center text-white shadow-md shadow-amber-600/30">
              <MessageSquare className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white">Bandeja de Mensajes</h3>
                <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-mono text-[10px] flex items-center gap-1 font-bold">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  En vivo
                </span>
              </div>
              <p className="text-xs text-stone-400">
                Chats de clientes para {collaborator.name}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl bg-stone-800 hover:bg-stone-700 text-stone-300 transition cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Informative notification */}
        <div className="bg-amber-50 border-b border-amber-200/80 p-3 text-xs text-amber-950 flex items-center gap-2">
          <HardHat className="w-4 h-4 text-amber-600 shrink-0" />
          <span>
            Estás conectado como <b>{collaborator.name}</b> ({collaborator.specialtyTitle}). Aquí recibes los mensajes que los clientes envían desde sus celulares.
          </span>
        </div>

        {/* Content */}
        <div className="p-4 overflow-y-auto flex-1 space-y-3">
          {/* Main active conversation card */}
          <div 
            onClick={() => {
              onClose();
              onOpenChat(collaborator, chats[0]?.chatId);
            }}
            className="p-4 rounded-2xl border-2 border-amber-500 bg-amber-50/40 hover:bg-amber-50 transition cursor-pointer flex items-center justify-between gap-3 shadow-xs"
          >
            <div className="flex items-center gap-3 min-w-0">
              <div className="w-11 h-11 rounded-2xl bg-stone-900 text-amber-400 flex items-center justify-center shrink-0">
                <User className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-extrabold text-stone-900 text-sm">
                    {chats[0]?.lastSenderName ? `Chat con ${chats[0].lastSenderName}` : 'Canal Principal de Clientes'}
                  </span>
                  <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                    Activo
                  </span>
                </div>
                <p className="text-xs text-stone-600 truncate mt-0.5">
                  {chats[0]?.lastMessage 
                    ? `"${chats[0].lastMessage}"`
                    : 'Toca para abrir la sala de chat en vivo con clientes'}
                </p>
                {chats[0]?.lastMessageTime && (
                  <div className="text-[10px] text-stone-400 flex items-center gap-1 mt-1 font-mono">
                    <Clock className="w-3 h-3" />
                    <span>{chats[0].lastMessageTime}</span>
                  </div>
                )}
              </div>
            </div>

            <div className="shrink-0 flex items-center gap-1 text-amber-600 font-bold text-xs">
              <span>Abrir Chat</span>
              <ChevronRight className="w-4 h-4" />
            </div>
          </div>

          {/* If there are other chats */}
          {chats.length > 1 && (
            <div className="space-y-2 mt-4">
              <div className="text-xs font-bold text-stone-500 uppercase tracking-wider px-1">
                Otras conversaciones registradas:
              </div>
              {chats.slice(1).map((chat) => (
                <div
                  key={chat.chatId}
                  onClick={() => {
                    onClose();
                    onOpenChat(collaborator, chat.chatId);
                  }}
                  className="p-3 bg-stone-50 hover:bg-stone-100 rounded-xl border border-stone-200 transition cursor-pointer flex items-center justify-between"
                >
                  <div className="min-w-0">
                    <div className="text-xs font-bold text-stone-800 truncate">
                      {chat.lastSenderName || 'Cliente'}
                    </div>
                    <div className="text-[11px] text-stone-500 truncate">
                      {chat.lastMessage}
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-stone-400 shrink-0" />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-stone-50 border-t border-stone-200 flex items-center justify-between">
          <div className="text-xs text-stone-500 flex items-center gap-1">
            <Radio className="w-3.5 h-3.5 text-emerald-600 animate-pulse" />
            <span>Sincronización automática con Firestore</span>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 bg-stone-200 hover:bg-stone-300 text-stone-800 text-xs font-bold rounded-xl transition cursor-pointer"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};
